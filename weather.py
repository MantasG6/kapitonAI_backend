import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import json


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def forecast(coordinates):
	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": coordinates.lat, 
		"longitude": coordinates.lon,
		"hourly": ["temperature_2m", "rain", "wind_speed_10m", "wind_direction_10m"],
		"forecast_days": 3,
		"temporal_resolution": "hourly_3"
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_rain = hourly.Variables(1).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
	hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["date"] = [d.strftime('%Y-%m-%d %H:%M') for d in hourly_data["date"]]
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["rain"] = hourly_rain
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

	hourly_dataframe = pd.DataFrame(data = hourly_data)

	return hourly_dataframe.to_json()

def marine(coordinates):
	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://marine-api.open-meteo.com/v1/marine"
	params = {
		"latitude": coordinates.lat,
		"longitude": coordinates.lon,
		"hourly": ["wave_height", "wave_direction"],
		"forecast_days": 3,
		"temporal_resolution": "hourly_3"
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()
	hourly_wave_direction = hourly.Variables(1).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s"),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	hourly_data["date"] = [d.strftime('%Y-%m-%d %H:%M') for d in hourly_data["date"]]
	hourly_data["wave_height"] = hourly_wave_height
	hourly_data["wave_direction"] = hourly_wave_direction


	hourly_dataframe = pd.DataFrame(data = hourly_data)

	return hourly_dataframe.to_json()