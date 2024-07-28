from sqlalchemy import Enum
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from database.models import DbPost, DbVote


class voteType(str, Enum):
    upVote = "Upvote"
    downVote = "Downvote"

def upVote(db: Session, post_id: int,user_id: int):

    post = db.query(DbPost).filter(DbPost.postid == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote = DbVote(
        voteType='Upvote',
        postId = post_id,
        userId = user_id
    )

    db.add(vote)
    post.voteCount += 1
    db.commit()
    db.refresh(post)

    return {"postId": post_id, "voteCount": post.voteCount}

def downVote(db: Session, post_id: int,user_id: int):
    post = db.query(DbPost).filter(DbPost.postid == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote = DbVote(
        voteType='Downvote',
        postId=post_id,
        userId=user_id
    )

    db.add(vote)
    post.voteCount -= 1
    db.commit()
    db.refresh(post)

    return {"postId": post_id, "voteCount": post.voteCount}
