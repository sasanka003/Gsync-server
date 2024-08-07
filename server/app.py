from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from database import models
from database.database import engine, init_redis, redis_close
from router import user, posts, plantations,login, comments

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    #init_redis()
    yield
    #redis_close()


app = FastAPI(lifespan=lifespan)
app.include_router(login.router)
app.include_router(user.router)
app.include_router(posts.router)
app.include_router(plantations.router)
app.include_router(comments.router)


@app.get('/')
def root():
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

app.mount('/documents', StaticFiles(directory='documents'), name='documents')