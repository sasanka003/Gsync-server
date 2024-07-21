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