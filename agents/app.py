import random
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import MessageSchema
import logfire
import uvicorn
from agents.rag import rag_agent
from agents.core import research_agent
from crew import parse_agricultural_data
from crews.enterprise_crew.enterprise_crew import EnterpriseAnalystCrew
from crews.iot_crew.iot_crew import IotAnalystCrew
from pydantic import BaseModel
from services import fm

logfire.configure()

app = FastAPI(
    title="Gsync Assistant",
    description="Gsync Assistant Microservice",
    version="0.1"
)
logfire.instrument_fastapi(app)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class JsonOutput(BaseModel):
    output: str


def generate_plant_data():
    # Generate random values within specified ranges
    plant_type = "capscicum"
    temperature = round(random.uniform(27, 30), 1)
    humidity = round(random.uniform(66, 70), 1)
    light_intensity = round(random.uniform(23000, 25000))
    co2_levels = round(random.uniform(400, 600))

    # Create formatted string
    data_string = f"{plant_type}, temperature {temperature} celcius, humidity {humidity}, light intensity {light_intensity} lux, Co2 levels {co2_levels}ppm"

    return data_string



@app.get('/chat/research', response_model=JsonOutput)
def chat_research(query: str = Query(...)):
    try:
        research_results = research_agent.run(
            message=query
        )
        return JsonOutput(output=research_results.content)
    except:
        return JsonOutput(output="not available right now")


@app.get('/chat/rag', response_model=JsonOutput)
def chat_rag(query: str = Query(...)):
    try:
        rag_results = rag_agent.run(
            message=query
        )
        return JsonOutput(output=rag_results.content)
    except:
        return JsonOutput(output="not available right now")


@app.get('/chat/enterprise/admin')
async def chat_ent_admin(background_task: BackgroundTasks):
    var_dict = parse_agricultural_data()

    try:
        result = EnterpriseAnalystCrew().crew().kickoff(
            inputs={
                "client_name": var_dict["farm_name"],
                "location": var_dict["farm_location"],
                "crop_list": var_dict["crop_yields"],
                "finance_data": f"operational costs: {var_dict["operational_costs"]}, revenue: {var_dict["revenue"]}, market_info: {var_dict["market_info"]}"
            }
        )
        
        message = MessageSchema(
            subject="AI Agent generated Finacial report",
            recipients=["visithkumarapperuma@gmail.com"],
            template_body={"markdown_content": result},
            subtype="html"
        )

        background_task.add_task(fm.send_message, message, template_name="financial_report.html")
        return JsonOutput(output=f"Your financial report: {result}")
    except:
        return JsonOutput(output="You have already reached the limit for your Quarterly financial analysis Generation, Contact Gsync customer service for extension.")


@app.get('/chat/iot', response_model=JsonOutput)
def chat_ent_user():
    iot_data = generate_plant_data()
    result = IotAnalystCrew().crew().kickoff(inputs={
        "plant_data": iot_data
    })
    return JsonOutput(output=f"your cultivation report: {result}")



if __name__ == "__main__":
    status = uvicorn.run(app, host="0.0.0.0", port=88)
    if status:
        logfire.info("Assistant Microservice up and running")
