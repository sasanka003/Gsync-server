from schemas.post import PostBase
from sqlalchemy.orm.session import Session
from database.models import DbPost
import datetime
from fastapi import HTTPException, status

def create(db: Session, request: PostBase):
  new_post = DbPost(
    title = request.title,
    description = request.description,
    image = request.image,
    dateshared = datetime.datetime.now(),
    userid = request.userid
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

def get_all(db: Session):
  return db.query(DbPost).all()

def delete(db: Session, id: int): # pass user_id: int
  post = db.query(DbPost).filter(DbPost.postid == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id {id} not found')
  if post.userId != 1: # 1 means user_id
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='Only post creator can delete post')

  db.delete(post)
  db.commit()
  return 'ok'