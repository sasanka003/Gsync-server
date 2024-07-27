from pydantic import BaseModel
from datetime import datetime

from database.db_post import PostType


class PostDisplay(BaseModel):
  postid: int
  title: str
  content: str
  media: str
  createdAt: datetime
  userid: int
  parentPostId:int
  postType:PostType
  class Config():
    orm_mode = True