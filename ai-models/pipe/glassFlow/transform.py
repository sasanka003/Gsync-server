import os 
from phi.agent import Agent
from pydantic import BaseModel
from pydantic.fields import Field
from openai import OpenAI
from dotenv import load_dotenv
from phi.model.openai import OpenAIChat
from supabase import create_client, Client
import base64
load_dotenv()


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def handler(data):
    supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    result, parsed = get_ai_results(
        base64_image=data["base64_image"],
        plant=data["plant"],
        location=data["location"],
        weather=data["weather"],
        temperature=data["temperature"]
    )
    

    data = {
        "image_id": data["image_id"],
        "sensor_id": data["sensor_id"], 
        "plantation_id": data["plantation_id"],  
        "prediction_details": result, 
        "pest": parsed.pest,
        "weed": parsed.weed,
        "disease": parsed.disease
    }

    response = supabase.table("predictions").insert(data).execute()

    return result


def get_ai_results(base64_image, plant, location, weather, temperature):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    agent = Agent(
        name="agriculture specialist agent",
        model=OpenAIChat(temperature=0),
        introduction="You are an expert in Srilankan agriculture field and has deep experience in identifying pest, diseases and weeds through your yeats of experience.",
        description="""You as an expert with deep knowledge in Srilankan agriculture. using Your expertise you will determine if there are any pest, diseases or weeds in the provided picture.""",
        guidelines=[
        "If you are not sure say you are uncertain",
        "If everything looks healthy say that it is healthy",
        "Think through and plan the process to derive conclusion",
        "Always remember that you will only be given images from plants grown in srilanka",
        "when uncertain try to provide the most probable disease/weed/pest"],
        task="""
        You are provided with the following data.\n
            - picture of the plant
            - name of the plant
            - current location within srilanka
            - current weather
            - IoT device readings of temperature of the plantbed.
            - current date.
        Based on these details you will come to the conclusion if there are any pest, disease or any weeds.
        your output must contain\n
            disease: disease names or healthy or uncertain
            weed: weed name or healthy or uncertain
            pest: pest names or healthy or uncertain
            summary: ten point summary 
            precautions: list of precations
        """,
        add_datetime_to_instructions=True
    )

    result = agent.run(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"plant: {plant}, location: {location}, weather: {weather}, IoT reading (temperature): {temperature}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ]
    )

    class OutputData(BaseModel):
        pest: bool = Field(description="deose the plant have a pest or not, if uncertain or yes then true, else false")
        weed: bool = Field(description="deose the plant have a weed or not, if uncertain or yes then true, else false")
        disease: bool = Field(description="deose the plant have disease or not, if uncertain or yes then true, else false")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract the prediction information."},
            {"role": "user", "content": result.content},
        ],
        response_format=OutputData,
    )

    return result.content, completion.choices[0].message.parsed


result = handler(
   {
        "image_id": 2,
        "base64_image": encode_image("../images/a-Wilt-in-Capsicum.jpg"),
        "plant": "capscicum",
        "location": "Colombo",
        "weather": "31 celcius",
        "temperature": "27 celcius",
        "sensor_id": 234,
        "plantation_id": 1,  
   }
)

print(result)
