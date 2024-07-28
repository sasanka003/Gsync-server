from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from database import db_votes
from database.database import get_db

router = APIRouter(
    prefix='/votes',
    tag=['votes']
)

# Upvote a post
@router.get("/{post_id}/upvote")
def upvote_post(post_id: int,db: Session = Depends(get_db),token: dict = Depends(verify_token),current_user: UserAuth = Depends(get_current_user)):
    return db_votes.upVote(db,post_id,current_user.userId)

# Downvote a post
@router.get("/{post_id}/downvote")
def downvote_post(post_id: int,db: Session = Depends(get_db),token: dict = Depends(verify_token),current_user: UserAuth = Depends(get_current_user)):
    return db_votes.downVote(db,post_id,current_user.userId)