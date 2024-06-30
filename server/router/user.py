from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from database import db_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('', )
def create_user(db: Session = Depends(get_db)):
    return {"message": "User created successfully"}
