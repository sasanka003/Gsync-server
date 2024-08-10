from sqlalchemy import Enum
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from database.models import DbVote
from pydantic import BaseModel
from pydantic.types import UUID4
from redis_om import HashModel
from redis_om import Field as RedisField
from database.database import get_redis_client


class VoteRequest(BaseModel):
    post_id: int | None
    comment_id: int | None
    user_id: UUID4
    vote_type: str

class VoteType(str, Enum):
    Upvote = "Upvote"
    Downvote = "Downvote"

class VoteBase(BaseModel):
    post_id: int
    user_id: str
    comment_id: int 
    vote_type: VoteType


class UserVote(HashModel):
    user_id: str = RedisField(index=True)
    post_id: int = RedisField(index=True)
    vote_type: VoteType
    class Meta:
        detabase = get_redis_client()

class AggregateVoteCount(HashModel):
    post_id: int = RedisField(index=True)
    upvotes: int
    downvotes: int
    class Meta:
        database = get_redis_client()



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
    
def update_vote_cache(post_id: int, user_id: str, vote_type: VoteType):
    user_vote = UserVote(user_id=user_id, post_id=post_id, vote_type=vote_type)
    user_vote.save()

    vote_count = AggregateVoteCount.get(post_id=post_id)
    if not vote_count:
        vote_count = AggregateVoteCount(post_id=post_id, upvotes=0, downvotes=0)
    if vote_type == VoteType.Upvote:
        vote_count.upvotes += 1
    else:
        vote_count.downvotes += 1
    vote_count.save()
