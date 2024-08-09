from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from services.topic_extractor import scheduled_update_trending_topics

from database import models
from database.database import engine, init_redis, redis_close
from router import user, posts, plantations,login, comments

from fastapi.middleware.cors import CORSMiddleware

scheduler = AsyncIOScheduler()
scheduler.add_job(
    func=scheduled_update_trending_topics,
    trigger=IntervalTrigger(hours=12),
    id='update_trending_topics_job',
    name='Update trending topics every 12 hours',
    replace_existing=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    scheduler.start()
    # init_redis()
    yield
    # redis_close()
    scheduler.shutdown()


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