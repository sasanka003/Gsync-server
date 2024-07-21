from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database import db_user
from auth.authentication import verify_token

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('', )
def create_user(db: Session = Depends(get_db)):
    return {"message": "User created successfully"}

@router.get("/{user_id}")
async def get_user_profile(user_id: str, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    return {"message": "User profile retrieved successfully"}
