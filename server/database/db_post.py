from typing import Optional
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from enum import Enum
from sqlalchemy.orm.session import Session
from database.models import DbPost, DbUser
import datetime
from pydantic import BaseModel
from fastapi import HTTPException, status, UploadFile, File
from redis_om import HashModel
from redis_om import Field as RedisField
from database import get_redis_client
from datetime import datetime
import uuid

class PostType(str, Enum):
    question = "Question"
    answer = "Answer"

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class PostBase(BaseModel):
  title: str
  content:str
  post_type:PostType
  user_id: uuid.UUID
  parent_post_id:Optional[int] = None


class PostMetaCache(HashModel):
    post_id: int = RedisField(index=True)
    title: str
    content: str
    parent_post_id: Optional[int]
    post_type: PostType
    class Meta:
        database = get_redis_client()



async def create(db: Session, title: str, content: str, post_type: PostType, user_id: uuid.UUID, parent_post_id: Optional[int], file: Optional[UploadFile] = None):
    # Check if the user exists
    user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if post_type not in [PostType.question, PostType.answer]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post type")

    file_url = None
    if file:
        image_content = await file.read()
        file_name = file.filename

        response = supabase.storage.from_('post_img').upload(file_name, image_content)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        # Extract the file URL from the response
        file_url = response.json().get('Key')

        if not file_url:
            raise HTTPException(status_code=500, detail="Failed to retrieve file URL from the response")

    new_post = DbPost(
        title=title,
        content=content,
        media=file_url,
        post_type=post_type,
        user_id=user_id,
        parent_post_id=parent_post_id,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session):
  return db.query(DbPost).all()

def delete(db: Session, post_id: int,user_id: uuid.UUID):
  post = db.query(DbPost).filter(DbPost.post_id == post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  if str(post.userId) != str(user_id):
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