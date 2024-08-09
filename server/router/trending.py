from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db, get_redis_client
from redis import Redis
from services.topic_extractor import get_trending_topics


router = APIRouter(
    prefix="/trending",
    tags=["trending"]
)


@router.get("/topics", description="get cached trending topics", response_description="sorted list of top 10 trending topics with the count", status_code=status.HTTP_200_OK)
async def get_trending_topics(db: Session = Depends(get_db), redis: Redis = Depends(get_redis_client)):
    """
    Get the top 10 trending topics from the cache

    """
    topics_json = get_trending_topics(db, redis)
    return {"trending_topics": topics_json}
