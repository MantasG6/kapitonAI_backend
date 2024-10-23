from groq import Groq
from extractData import getConditionsArray
import json
from pydantic import BaseModel

class Coordinates(BaseModel):
    lat: int
    lon: int

class Destination(BaseModel):
    coordinates: Coordinates
    name: str
    comfortLevel: str
    distance: float
    time: str


conditionsArray = getConditionsArray()
conditions = conditionsArray[0]

client = Groq(
    api_key="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"
)
completion = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {
            "role": "system",
                "content": "You are a sailboat expert, providing useful insights to the captain in JSON.\n"
                # Pass the json schema to the model. Pretty printing improves results.
                f" The JSON object must use the schema: {json.dumps(Destination.model_json_schema(), indent=2)} \n"
                "Distance should be in nautical miles and time should be in hours",
        },
        {
            "role": "user",
            "content": f"""
    <sailingData>
      <location>
          <name>Palaio Faliro</name>
          <region>Attica</region>
          <country>Greece</country>
          <lat>37.921</lat>
          <lon>23.709</lon>
          <tz_id>Europe/Athens</tz_id>
          <localtime_epoch>1729608957</localtime_epoch>
          <localtime>2024-10-22 17:55</localtime>
      </location>
      <forecast>
          <forecastday>
              <date>2024-10-22</date>
              <date_epoch>1729555200</date_epoch>
              <day>
                  <maxtemp_c>20.8</maxtemp_c>
                  <maxtemp_f>69.4</maxtemp_f>
                  <mintemp_c>12.7</mintemp_c>
                  <mintemp_f>54.9</mintemp_f>
                  <avgtemp_c>17</avgtemp_c>
                  <avgtemp_f>62.5</avgtemp_f>
                  <maxwind_mph>15</maxwind_mph>
                  <maxwind_kph>24.2</maxwind_kph>
                  <totalprecip_mm>0</totalprecip_mm>
                  <totalprecip_in>0</totalprecip_in>
                  <totalsnow_cm>0</totalsnow_cm>
                  <avgvis_km>10</avgvis_km>
                  <avgvis_miles>6</avgvis_miles>
                  <avghumidity>57</avghumidity>
                  <tides>
                      <tide>
                          <tide_time>2024-10-22 03:38</tide_time>
                          <tide_height_mt>0.20</tide_height_mt>
                          <tide_type>LOW</tide_type>
                      </tide>
                      <tide>
                          <tide_time>2024-10-22 10:34</tide_time>
                          <tide_height_mt>0.70</tide_height_mt>
                          <tide_type>HIGH</tide_type>
                      </tide>
                      <tide>
                          <tide_time>2024-10-22 15:56</tide_time>
                          <tide_height_mt>0.30</tide_height_mt>
                          <tide_type>LOW</tide_type>
                      </tide>
                      <tide>
                          <tide_time>2024-10-22 22:53</tide_time>
                          <tide_height_mt>0.70</tide_height_mt>
                          <tide_type>HIGH</tide_type>
                      </tide>
                  </tides>
                  <condition>
                      <text>Partly Cloudy </text>
                      <icon>//cdn.weatherapi.com/weather/64x64/day/116.png</icon>
                      <code>1003</code>
                  </condition>
                  <uv>5</uv>
              </day>
          </forecastday>
      </forecast>
      <boatInfo>
        <boatType>Cruising Yacht</boatType>
        <length>12.5</length>
        <width>4.2</width>
        <waterlineDepth>1.8</waterlineDepth>
        <mastHeight>16.0</mastHeight>
        <displacement>8500</displacement>
        <keelType>Fin keel</keelType>
        <sailArea>75</sailArea>
        <enginePower>25</enginePower>
        <fuelCapacity>200</fuelCapacity>
        <rudderType>Skeg-hung</rudderType>
        <crewSize>6</crewSize>
        <hullMaterial>Fiberglass</hullMaterial>
      </boatInfo>
      <experience>
        <yearsOfExperience>7</yearsOfExperience>
        <experienceLevel>Intermediate</experienceLevel>
        <typeOfWaterSailed>
          <waterType>Coastal</waterType>
          <waterType>Inland Waters</waterType>
        </typeOfWaterSailed>
        <typesOfBoatsSailed>
          <boatType>Monohull</boatType>
          <boatType>Dinghy</boatType>
        </typesOfBoatsSailed>
        <certifications>
          <certification>ASA 101 Basic Keelboat Sailing</certification>
          <certification>ASA 103 Coastal Navigation</certification>
        </certifications>
        <totalMilesSailed>2500</totalMilesSailed>
        <soloSailingExperience>No</soloSailingExperience>
        <sailingCoursesTraining>
          <course>Coastal Cruising</course>
          <course>Advanced Seamanship</course>
        </sailingCoursesTraining>
      </experience>
    </sailingData>

    Based on provided location, forecast and boatInfo could you please provide me with 3 best locations to travel knowing I want my travel to be comfortable and take me around 6 hours?
    """
        }
    ],
    temperature=1,
    max_tokens=8000,
    top_p=1,
    stream=False,
    stop=None,
    seed=42,
    response_format={"type": "json_object"}
)

def get_result():
    return completion.choices[0].message.content
