import base64
from vertexai.generative_models import GenerativeModel, Part, SafetySetting, GenerationConfig


def generate(conditions):
    model = GenerativeModel(
        "gemini-1.5-pro-002",
    )

    text1 = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
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
    Course (give me a degree value)

    Could you also provide all the information only in Json format and no additional text?"""

    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    my_response = ''
    for response in responses:
        my_response += response.text

    return my_response

response_schema = {
    "type": "object",
    "properties": {
        "mainSailPosition": {
            "type": "number",
            "description": "Main sail position number (-5 to 5)"
        },
        "jibSailPosition": {
            "type": "number",
            "description": "Jib sail position number (-5 to 5)"
        },
        "shortNoteSails": {
            "type": "string",
            "description": "SHORT note about how should I change sail positions"
        },
        "course": {
            "type": "number",
            "description": "Course in degrees"
        },
        "shortNoteCourse": {
            "type": "string",
            "description": "SHORT note about how should I change course"
        }
    },
    "required": [
        "mainSailPosition",
        "jibSailPosition",
        "shortNoteSails",
        "course",
        "shortNoteCourse"
    ]
}

generation_config = GenerationConfig(
    max_output_tokens=8192,
    temperature= 1,
    top_p=0.95,
    response_mime_type= "application/json",
    response_schema= response_schema,
)

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    ),
]