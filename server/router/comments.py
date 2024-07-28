from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from database import db_comment
from database.database import get_db
# from auth.authentication import verify_token
# from database.db_comment import CommentCreate
from database.db_comment import CommentCreate

router = APIRouter(
    prefix='/posts',
    tags=['posts', 'comments']
)

@router.get('/{post_id}/comments', description='Get comments of a post when authorised or non-authoried', response_description="all comments of a post")
def get_comments(post_id: int, db: Session = Depends(get_db),token: Optional[dict] = Depends(verify_token)): #token: Optional[dict] = Depends(verify_token)

    if token:
        return db_comment.get_comments(post_id, db)
    else:
        pass


@router.post('/{post_id}/comments', description='Create a comment', response_description="created comment & status", status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    request: CommentCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    return db_comment.create_comment(db,request)

@router.put('/{post_id}/comments/{comment_id}', description='Edit a comment', response_description="Comment updated status")
def update_comment(
    post_id: int,
    comment_id: int,
    request: CommentCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    return db_comment.update_comment(comment_id, request, db)
