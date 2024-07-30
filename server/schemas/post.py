from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from redis_om import HashModel
from database.database import get_redis_client
import pytz

from database.db_post import PostType
from sqlalchemy.dialects.postgresql import UUID
import uuid


class PostDisplay(BaseModel):
  post_id: int
  title: str
  content: str
  media: Optional[str] = None
  created_at: datetime
  user_id: uuid.UUID
  parent_post_id: Optional[int] = None
  post_type:PostType
  class Config:
    from_attributes = True


class VoteCache(HashModel):
    post_id: int 
    vote_count: int
    class Meta:
        detabase = get_redis_client()


class CommentCache(HashModel):
    post_id: int
    comment_id: int
    content: str
    last_updated: datetime = datetime.now(pytz.utc)
    class Meta:
        database = get_redis_client()


class PostCache(HashModel):
    post_id: int
    title: str
    content: str
    media: str
    post_type: str
    user_id: str
    parent_post_id: int
    created_at: datetime = datetime.now(pytz.utc)
    last_updated: datetime = datetime.now(pytz.utc)
    class Meta:
        database = get_redis_client()
