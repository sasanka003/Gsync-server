from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import db_post
from database.database import get_db
from schemas.post import PostBase, PostDisplay

router = APIRouter(
    prefix='/post',
    tags=['post']
)

@router.post('',response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db)):
    return db_post.create(db,request)