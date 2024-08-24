from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from database import db_post
from database.database import get_db
from database.db_post import PostBase, PostType
from schemas.post import PostDisplay, PostCreateDisplay
from typing import List
from auth.authentication import verify_token, get_current_user
import uuid

router = APIRouter(
    prefix='/post',
    tags=['post']
)

@router.post('/create',response_model=PostCreateDisplay) 
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    post_type: PostType = Form(...),
    user_id: uuid.UUID = Form(...),
    tags: Optional[List[str]] = Form([]),
    parent_post_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user)
):
    
    return await db_post.create(
        db, 
        title,
        content, 
        post_type, 
        user_id, # current_user.user_id, 
        parent_post_id, 
        file
    )

@router.get("/all",response_model=List[PostDisplay], deprecated=True)
def get_all_posts(db: Session = Depends(get_db)): #token: dict = Depends(verify_token)
    return db_post.get_all(db)

# Delete post
@router.delete("/delete/{post_id}") #@router.delete("/{id}")
def delete_post(post_id:int, db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    return db_post.delete(db,post_id,current_user.user_id)

# Update a post
@router.put("/{post_id}", response_model=PostDisplay)
def update_post(post_id: int, request: PostBase, db: Session = Depends(get_db),token: dict = Depends(verify_token)):
    return  db_post.update(db, post_id, request)


# Get a post
@router.get("/top/", response_model=List[PostDisplay])
def get_top_posts(
    limit: int = Query(10, gt=1, le=100, description="post limit per req."), 
    offset: int = Query(0, ge=0, description="post offset in current request."), 
    db: Session = Depends(get_db)):
    top_posts = db_post.get_top_posts(db, limit=limit, offset=offset)
    return [
        PostDisplay(
            **post.__dict__,
            user_name=user_name,
            upvote_count=upvote_count,
            downvote_count=downvote_count,
            comment_count=comment_count
        ) for post, user_name, upvote_count, downvote_count, comment_count in top_posts
    ]