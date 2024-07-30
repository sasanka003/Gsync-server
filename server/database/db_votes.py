from sqlalchemy import Enum
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from database.models import DbPost, DbVote
from pydantic import BaseModel


class VoteType(str, Enum):
    Upvote = "Upvote"
    Downvote = "Downvote"


class VoteBase(BaseModel):
    post_id: int
    user_id: str
    comment_id: int 
    vote_type: VoteType


def get_post_votes(db: Session, post_id: int):
    return db.query(DbVote).filter(DbVote.post_id == post_id).all()

def get_comment_votes(db: Session, comment_id: int):
    return db.query(DbVote).filter(DbVote.comment_id == comment_id).all()

def get_vote_count(db: Session, post_id: int = None, comment_id: int = None):
    if post_id:
        upvotes = db.query(DbVote).filter(DbVote.post_id == post_id, DbVote.vote_type == 'Upvote').count()
        downvotes = db.query(DbVote).filter(DbVote.post_id == post_id, DbVote.vote_type == 'Downvote').count()
        return {'upvotes': upvotes, 'downvotes': downvotes}
    elif comment_id:
        upvotes = db.query(DbVote).filter(DbVote.comment_id == comment_id, DbVote.vote_type == 'Upvote').count()
        downvotes = db.query(DbVote).filter(DbVote.comment_id == comment_id, DbVote.vote_type == 'Downvote').count()
        return {'upvotes': upvotes, 'downvotes': downvotes}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    
def update_vote(db: Session, post_id: int = None, comment_id: int = None, user_id: str = None, vote_type: VoteType = None):
    if post_id:
        vote = db.query(DbVote).filter(DbVote.post_id == post_id, DbVote.user_id == user_id).first()
        if vote:
            if vote.vote_type == vote_type:
                db.delete(vote)
                db.commit()
                return 'deleted'
            else:
                vote.vote_type = vote_type
                db.commit()
                return 'updated'
        else:
            new_vote = DbVote(post_id=post_id, user_id=user_id, vote_type=vote_type)
            db.add(new_vote)
            db.commit()
            return 'created'
    elif comment_id:
        vote = db.query(DbVote).filter(DbVote.comment_id == comment_id, DbVote.user_id == user_id).first()
        if vote:
            if vote.vote_type == vote_type:
                db.delete(vote)
                db.commit()
                return 'deleted'
            else:
                vote.vote_type = vote_type
                db.commit()
                return 'updated'
        else:
            new_vote = DbVote(comment_id=comment_id, user_id=user_id, vote_type=vote_type)
            db.add(new_vote)
            db.commit()
            return 'created'
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
