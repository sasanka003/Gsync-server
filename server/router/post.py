from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import db_post
from database.database import get_db
from schemas.post import PostBase, PostDisplay
from typing import List


router = APIRouter(
    prefix='/post',
    tags=['post']
)

@router.post('',response_model=PostDisplay) #  get userid form jwt
def create_post(request: PostBase, db: Session = Depends(get_db)):
    return db_post.create(db,request)

@router.get("/all",response_model=List[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)

@router.get("/delete/{id}")
def delete_post(id:int,db: Session = Depends(get_db)): # current_user: UserAuth = Depends(get_current_user)
    return db_post.delete(db,id) #get userid form jwt
