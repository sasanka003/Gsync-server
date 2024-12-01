import random
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import logfire
import uvicorn
from agents.rag import rag_agent
from agents.core import research_agent
from crew import parse_agricultural_data
from crews.enterprise_crew.enterprise_crew import EnterpriseAnalystCrew
from crews.iot_crew.iot_crew import IotAnalystCrew

logfire.configure(project_name='gsync-assistant')

app = FastAPI(
    title="Gsync Assistant",
    description="Gsync Assistant Microservice",
    version="0.1"
)
logfire.instrument_fastapi(app)

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



@app.get('/chat/research')
def chat_research(query: str = Query(...)):
    try:
        research_results = research_agent.run(
            message=query
        )
        return {"message": research_results.content}
    except:
        return {"message": "not available right now"}


@app.get('chat/rag')
def chat_rag(query: str = Query(...)):
    try:
        rag_results = rag_agent.run(
            message=query
        )
        return {"message": rag_results.content}
    except:
        return {"message": "not available right now"}


@app.get('/chat/enterprise/admin')
def chat_ent_admin():
    var_dict = parse_agricultural_data()

    result = EnterpriseAnalystCrew().crew().kickoff(
        inputs={
            "client_name": var_dict["farm_name"],
            "location": var_dict["farm_location"],
            "crop_list": var_dict["crop_yields"],
            "finance_data": f"operational costs: {var_dict["operational_costs"]}, revenue: {var_dict["revenue"]}, market_info: {var_dict["market_info"]}"
        }
    )
    return {"message": result}

@app.get('/chat/iot')
def chat_ent_user():
    iot_data = generate_plant_data()
    try:
        result = IotAnalystCrew().crew().kickoff(inputs={
            "plant_data": iot_data
        })
        return {"message": result}
    except:
        return {"message": "iot analysis waiting in queue, sending via email."}


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

if __name__ == "__main__":
    status = uvicorn.run(app, host="0.0.0.0", port=88)
    if status:
        logfire.info("Assistant Microservice up and running")
