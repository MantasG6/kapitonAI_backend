from groq import Groq
import json
from pydantic import BaseModel
from pydantic import Field
from weather import forecast, marine
from dict2xml import dict2xml

class Coordinates(BaseModel):
    lat: float
    lon: float

class Destination(BaseModel):
    coordinates: Coordinates
    name: str = Field(description="Destination port name")
    comfortLevel: str = Field(description="Comfort level of the sailor (Too Little Challenge, Comfortable Sailing, Moderate Sailing, Challenging Sailing, Extreme Sailing, Too Extreme to Sail)")
    distance: float = Field(description="Distance to the destination port in nautical miles")
    time: str = Field(description="Time to reach destination port from current location in hours (00:00)")

coords = Coordinates(lat=37.921, lon=23.709)

forecast_json = forecast(coords)
marine_json = marine(coords)

forecast_dict = json.loads(forecast_json)
marine_dict = json.loads(marine_json)

forecast_xml = dict2xml(forecast_dict, wrap="forecast", indent="  ")
marine_xml = dict2xml(marine_dict, wrap="marine", indent="  ")

client = Groq(
    api_key="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"
)


messages = [
        {
            "role": "system",
                "content": "You are a sailboat expert, providing useful insights to the captain in JSON.\n"
                # Pass the json schema to the model. Pretty printing improves results.
                f" The JSON object must use the schema: {json.dumps(Destination.model_json_schema(), indent=2)}"
        },
        {
            "role": "user",
            "content": f"""
    <sailingData>
      <location>
          <name>Palaio Faliro</name>
          <region>Attica</region>
          <country>Greece</country>
          <lat>{coords.lat}</lat>
          <lon>{coords.lon}</lon>
          <tz_id>Europe/Athens</tz_id>
          <localtime>2024-11-12 10:55</localtime>
      </location>
      {forecast_xml}
      {marine_xml}
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

    Based on provided location, forecast and boatInfo could you please provide me with 5 destinations to travel with traveling time of 6 hours and different levels of comfort?
    """
        }
    ]



def get_result():
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=1,
        max_tokens=8000,
        top_p=1,
        stream=False,
        stop=None,
        seed=42,
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content