from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import db_votes
from database.db_votes import VoteRequest
from database.database import get_db

router = APIRouter(
    prefix='/votes',
    tag=['votes']
)


@router.get('/get_post_votes/{post_id}', description='get all votes of a post', response_description='upvote/downvote count')
def get_post_votes(post_id: int, db: Session = Depends(get_db)):
    try:
        votes_dict = db_votes.get_vote_count(db, post_id=post_id)
        return votes_dict
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.get('/get_comment_votes/{comment_id}', description='get all votes of a comment', response_description='upvote/downvote count')
def get_comment_votes(comment_id: int, db: Session = Depends(get_db)):
    try:
        votes_dict = db_votes.get_vote_count(db, comment_id=comment_id)
        return votes_dict
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.get('/get_post_votes/all/{post_id}', description='get all votes of a post', response_description='information on votes')
def get_post_votes(post_id: int, db: Session = Depends(get_db)):
    try:
        votes = db_votes.get_post_votes(db, post_id)
        return votes
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.get('/get_comment_votes/all/{comment_id}', description='get all votes of a comment', response_description='information on votes')
def get_comment_votes(comment_id: int, db: Session = Depends(get_db)):
    try:
        votes = db_votes.get_comment_votes(db, comment_id)
        return votes
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@router.post('/update_post_vote/{post_id}', description='update a vote', response_description='vote updated', status_code=status.HTTP_201_CREATED)
async def update_post_vote(post_id: int, user_id: str, vote_type: str, db: Session = Depends(get_db)):
    vote_type = db_votes.VoteType(vote_type=vote_type)
    try:
        action = db_votes.update_vote(db, post_id=post_id, user_id=user_id, vote_type=vote_type)
        db_votes.update_vote_cache(post_id=post_id,
                                   user_id=user_id, 
                                   vote_type=vote_type
                                )
        return {"message": f"Vote {action} successfully"}
    except Exception as e:
        return {"message": e}
    
@router.post('/update_comment_vote/{comment_id}', description='update a vote', response_description='vote updated', status_code=status.HTTP_201_CREATED)
async def update_comment_vote(comment_id: int, user_id: str, vote_type: str, db: Session = Depends(get_db)):
    try:
        vote = db_votes.update_vote(db, comment_id=comment_id, user_id=user_id, vote_type=vote_type)
        return {"message": f"Vote {vote} successfully"}
    except Exception as e:
        return {"message": e}
    