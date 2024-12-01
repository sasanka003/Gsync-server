from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import logfire
import uvicorn
from agents.rag import rag_agent
from agents.core import research_agent

logfire.configure(project_name='gsync-assistant')



app = FastAPI(
    title="Gsync Assistant",
    description="Gsync Assistant Microservice",
    version="0.1"
)
logfire.instrument_fastapi(app)



@app.get('/chat/research')
def chat_research(query: str = Query(...)):
    research_results = research_agent.run(
        message=query
    )
    return {"message": research_results.content}


@app.get('chat/rag')
def chat_rag(query: str = Query(...)):
    rag_results = rag_agent.run(
        message=query
    )
    return {"message": rag_results.content}


@app.get('/chat/enterprise/admin')
def chat_ent_admin():
    return {"message": "Hello World"}

@app.get('/chat/iot')
def chat_ent_user():
    return {"message": "Hello World"}


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
