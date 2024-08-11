from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
  post_type: PostType
  last_updated: Optional[datetime] = None
  tag: list[str] = []
  user_name: str
  upvote_count: int = 0
  downvote_count: int = 0
  comment_count: int = 0
  class Config:
    from_attributes = True
