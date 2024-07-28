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
  post_type:PostType
  class Config():
    orm_mode = True