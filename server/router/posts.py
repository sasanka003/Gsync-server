from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import db_post
from database.database import get_db
from database.db_post import PostBase
from schemas.post import PostDisplay
from typing import List
from auth.authentication import verify_token, get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)

@router.post('',response_model=PostDisplay) #response_model=PostDisplay
def create_post(request: PostBase, db: Session = Depends(get_db)): #token: dict = Depends(verify_token)
    return db_post.create(db,request)

@router.get("/all",response_model=List[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)): #token: dict = Depends(verify_token)
    return db_post.get_all(db)

# Delete post
@router.get("/delete/{post_id}") #@router.delete("/{id}")
def delete_post(post_id:int,db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    return db_post.delete(db,post_id,current_user.user_id)

# Update a post
@router.put("/{post_id}", response_model=PostDisplay)
def update_post(post_id: int, request: PostBase, db: Session = Depends(get_db),token: dict = Depends(verify_token)):
    return  db_post.update(db, post_id, request)



