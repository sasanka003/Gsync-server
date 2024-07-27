from datetime import datetime

import pydantic
from fastapi import HTTPException
from rich import status
from sqlalchemy.orm.session import Session
from pydantic import BaseModel
from database.models import DbComment, DbPost, DbUser


class CommentCreate(BaseModel):
    content: str
    user_id: int
    post_id: int

def create_comment(db: Session, request: CommentCreate):

    # Check if the post exists
    post = db.query(DbPost).filter(DbPost.postId == request.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Check if the user exists
    user = db.query(DbUser).filter(DbUser.userId == request.user_id).first() # no userId in DbUser
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_comment = DbComment(
        content = request.content,
        postId = request.post_id,
        userId = request.user_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh()
    return new_comment


def get_comments(post_id: int, db: Session):
    #Check if the post exists
    post = db.query(DbPost).filter(DbPost.postId == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comments = db.query(DbComment).filter(DbComment.postId == post_id).all()
    return comments

def update_comment(comment_id: int, request: CommentCreate, db: Session):

    # Retrieve the comment to update
    comment = db.query(DbComment).filter(DbComment.commentId == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    comment.content = request.content
    comment.lastUpdated = datetime.utcnow()

    db.commit()
    db.refresh(comment)

    return comment






