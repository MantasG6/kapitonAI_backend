from groq import Groq
from extractData import getConditionsArray
import json
from pydantic import BaseModel

class Response(BaseModel):
    mainSailPosition: int
    jibSailPosition: int
    shortNoteSails: str
    course: int
    shortNoteCourse: str


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
                f" The JSON object must use the schema: {json.dumps(Response.model_json_schema(), indent=2)}",
        },
        {
            "role": "user",
            "content": f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <sailingData>
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
      <conditions>
        <speedOverGround>{conditions.speedOverGround}</speedOverGround>
        <courseOverGround>{conditions.courseOverGround}</courseOverGround>
        <heelAngle>{conditions.heelAngle}</heelAngle>
        <windSpeed>{conditions.windSpeed}</windSpeed>
        <windDirection>{conditions.windDirection}</windDirection>
        <tideCurrent>
          <speed>{conditions.tideCurrent.speed}</speed>
          <direction>{conditions.tideCurrent.direction}</direction>
        </tideCurrent>
        <coordinates>
          <latitude>{conditions.coordinates.latitude}</latitude>
          <longitude>{conditions.coordinates.longitude}</longitude>
        </coordinates>
      </conditions>
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
      <goal>
        <coordinates>
          <latitude>35.459859</latitude>
          <longitude>23.590378</longitude>
        </coordinates>
        <performance>Comfort over speed</performance>
      </goal>
    </sailingData>

    <sail_positions>
      <position id=\"0\">
        <name>Into the wind</name>
      </position>
      <position id=\"-1\">
        <name>Close Hauled Port side</name>
      </position>
      <position id=\"-2\">
        <name>Close Reach Port side</name>
      </position>
      <position id=\"-3\">
        <name>Beam Reach Port side</name>
      </position>
      <position id=\"-4\">
        <name>Broad Reach Port side</name>
      </position>
      <position id=\"-5\">
        <name>Running Port side</name>
      </position>
      <position id=\"1\">
        <name>Close Hauled Starboard side</name>
      </position>
      <position id=\"2\">
        <name>Close Reach Starboard side</name>
      </position>
      <position id=\"3\">
        <name>Beam Reach Starboard side</name>
      </position>
      <position id=\"4\">
        <name>Broad Reach Starboard side</name>
      </position>
      <position id=\"5\">
        <name>Running Starboard side</name>
      </position>
    </sail_positions>

    Based on provided information, could you please give me tips on ACTIONS  (only if action is needed in that area):
    How should be the main sail position (Give me a position in a form of number -5 to 5 in provided sail_positions, but in description use ONLY ORIGINAL POSITION NAMES),
    How should be the jib sail position (Give me a position in a form of number -5 to 5 in provided sail_positions, but in description use ONLY ORIGINAL POSITION NAMES),
    Course (give me a degree value)"""
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

print(completion.choices[0].message.content)
