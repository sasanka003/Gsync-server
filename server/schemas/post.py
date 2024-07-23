from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
  title: str
  description: str
  image: str
  userid: str #  get userid from jwt

class PostDisplay(BaseModel):
  postid: int
  title: str
  description: str
  image: str
  dateshared: datetime
  userid: str
  class Config():
    orm_mode = True