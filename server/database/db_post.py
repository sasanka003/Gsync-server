from typing import Optional

from enum import Enum as PyEnum
from sqlalchemy.orm.session import Session
from database.models import DbPost, DbUser
import datetime
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import UUID
import uuid

from enum import Enum

class PostType(str, Enum):
    question = "Question"
    answer = "Answer"

class PostBase(BaseModel):
  title: str
  content:str
  media: Optional[str] = None  # media is optional and, if not provided, its default value is None.
  post_type:PostType
  user_id: uuid.UUID
  parent_post_id:Optional[int] = None


def create(db: Session, request: PostBase):

  # Check if the user exists
  user = db.query(DbUser).filter(DbUser.user_id == request.user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  new_post = DbPost(
    title = request.title,
    content = request.content,
    media = request.media,
    post_type=request.post_type,
    user_id=request.user_id,
    parent_post_id=request.parent_post_id,
    # created_at=datetime.utcnow()
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

def get_all(db: Session):
  return db.query(DbPost).all()

def delete(db: Session, post_id: int,user_id: int):
  post = db.query(DbPost).filter(DbPost.post_id == post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  if post.userId != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only post creator can delete post')

  db.delete(post)
  db.commit()
  return {"detail": "Post deleted successfully"}

def update(db: Session, post_id: int, request: PostBase):

  post = db.query(DbPost).filter(DbPost.post_id == post_id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {post_id} not found')
  if post.userId != request.userid:  # Ensure the user updating the post is the creator
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only post creator can update post')

  # Update the post fields
  if request.title is not None:
    post.title = request.title
  if request.content is not None:
    post.content = request.content
  if request.media is not None:
    post.media = request.media
  if request.postType is not None:
    post.postType = request.postType
  if request.parentPostId is not None:
    post.parentPostId = request.parentPostId

  #post.lastUpdated = datetime.utcnow()  # Assuming you have a lastUpdated field in your model

  db.commit()
  db.refresh(post)
  return post
