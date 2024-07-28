import pydantic
from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str
    user_id: int
    post_id: int
    