import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from redis_om import get_redis_connection, HashModel

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

def get_redis_client():
    return redis

def init_redis():
    # Ping Redis to check connection
    try:
        redis.ping()
        print("Successfully connected to Redis")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise

    # create indexes for models

def redis_close():
    redis.close()


def get_or_set_cache(key: str, value_func, expire_time=3600):
    cached_value = redis.get(key)
    if cached_value:
        return cached_value
    value = value_func()
    redis.setex(key, expire_time, value)
    return value
