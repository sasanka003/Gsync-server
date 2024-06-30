from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from database import models
from database.database import engine, init_redis
from router import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(user.router)


@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    #init_redis()


@app.get('/')
def root():
    return {"message": "Hello World"}


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/documents', StaticFiles(directory='documents'), name='documents')