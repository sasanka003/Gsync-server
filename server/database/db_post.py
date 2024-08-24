from typing import Optional
import os
import uuid
from dotenv import load_dotenv
from enum import Enum
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc, case
from sqlalchemy.orm.session import Session
from database.models import DbPost, DbUser, DbVote, DbTag, DbComment, post_tags
from database.database import get_redis_client, supabase
import datetime
from pydantic import BaseModel, Field
from fastapi import HTTPException, status, UploadFile, File
from redis_om import HashModel
from redis_om import Field as RedisField
from uuid import UUID


class PostType(str, Enum):
    question = "Question"
    answer = "Answer"


class PostBase(BaseModel):
  title: str = Field(..., description="Title of the post, must be between 5 and 50 characters.", max_length=50, min_length=5)
  content:str = Field(..., description="Content of the post, must be between 10 and 10000 characters.", max_length=10000, min_length=10)
  post_type:PostType = Field(default=PostType.question, description="Type of the post, either 'Question' or 'Answer'")
  user_id: UUID = Field(..., description="User ID of the post creator")
  parent_post_id:Optional[int] = Field(default=0, ge=0, description="ID of the parent post if the post is an answer to a question")


class PostMetaCache(HashModel):
    post_id: int = RedisField(index=True)
    title: str
    content: str
    parent_post_id: Optional[int]
    post_type: PostType
    class Meta:
        database = get_redis_client()



async def create(db: Session, title: str, content: str, post_type: PostType, user_id: UUID, parent_post_id: Optional[int] = None, file: Optional[UploadFile] = None):
    # Check if the user exists
    user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if post_type not in [PostType.question, PostType.answer]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post type")

    file_url = None
    if file:
        image_content = await file.read()
        original_filename = file.filename

        file_name = f"{user_id}_{uuid.uuid4()}_{original_filename}"

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


def get_top_posts_query(db: Session):
   return db.query(
    DbPost,
    DbUser.name.label('user_name'),
    func.count(case((DbVote.vote_type == 'Upvote', 1))).label('upvote_count'),
    func.count(case((DbVote.vote_type == 'Downvote', 1))).label('downvote_count'),
    func.count(DbComment.comment_id).label('comment_count')
  ).outerjoin(
    DbVote,
    DbPost.post_id == DbVote.post_id
  ).outerjoin(
    DbComment,
    DbPost.post_id == DbComment.post_id
  ).outerjoin(
    DbUser,
    DbPost.user_id == DbUser.user_id
  ).outerjoin(
    DbTag, 
    post_tags.c.tag_id == DbTag.tag_id
  ).options(
    joinedload(DbPost.tags)
  ).group_by(
    DbUser.name,
    DbPost.post_id
  )


def get_top_posts(db: Session, limit: int = 10, offset: int = 0):
  return get_top_posts_query(db).order_by(
    desc(func.count(DbVote.vote_id) + func.count(DbComment.comment_id)), 
    desc(DbPost.created_at)
  ).limit(limit).offset(offset).all()


def delete(db: Session, post_id: int, user_id: UUID):
  post = db.query(DbPost).filter(DbPost.post_id == post_id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  if post.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only post creator can delete post')
  if post.media:
    response = supabase.storage.from_('post_img').remove(post.media)
    if response.status_code != 200:
      raise HTTPException(status_code=response.status_code, detail="Error removing media from storage")

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
    if post.media:
      response = supabase.storage.from_('post_img').remove(post.media)
      if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error removing media from storage")
    post.media = request.media
  if request.post_type is not None:
    post.post_type = request.post_type
  if request.parent_post_id is not None:
    post.parent_post_id = request.parent_post_id

  post.last_updated = datetime.utcnow()  

  db.commit()
  db.refresh(post)
  return post


def get_trending_posts(db: Session):
  return  db.query(
                    DbPost.content, 
                    DbPost.title
          ).order_by(DbPost.created_at.desc()).limit(100).all()


def get_all_tags(db: Session, limit: int = 10):
  return db.query(DbTag.tag_name).limit(limit).all()


def filter_posts_by_tags(db: Session, tags: list, limit: int = 10, offset: int = 0):
  tags = [tag.lower() for tag in tags]
  return get_top_posts_query(db).filter(
    DbTag.tag_name.in_(tags)
  ).limit(limit).offset(offset).all()


def filter_post_by_most_recent(db: Session, days: int = None, limit: int = 10, offset: int = 0):
  posts = get_top_posts_query(db)

  if days is not None:
    posts = posts.filter(DbPost.created_at >= datetime.datetime.now() - datetime.timedelta(days=days))
  
  posts = posts.order_by(DbPost.created_at.desc()).limit(limit).offset(offset).all()
  return posts


def filter_post_by_votes(db: Session, limit: int = 10, vote_type: str = 'Upvote', offset: int = 0):
  return db.query(
    DbPost,
    DbUser.name.label('user_name'),
    func.count(case((DbVote.vote_type == 'Upvote', 1))).label('upvote_count'),
    func.count(case((DbVote.vote_type == 'Downvote', 1))).label('downvote_count'),
    func.count(DbComment.comment_id).label('comment_count')
  ).outerjoin(
    DbVote,
    (DbPost.post_id == DbVote.post_id) & (DbVote.vote_type == vote_type)
  ).outerjoin(
    DbComment,
    DbPost.post_id == DbComment.post_id
  ).outerjoin(
    DbUser,
    DbPost.user_id == DbUser.user_id
  ).outerjoin(
      DbTag, 
      post_tags.c.tag_id == DbTag.tag_id
  ).options(
    joinedload(DbPost.tags)
  ).group_by(
    DbUser.name,
    DbPost.post_id
  ).order_by(
    desc('vote_count')
  ).limit(limit).offset(offset).all()
