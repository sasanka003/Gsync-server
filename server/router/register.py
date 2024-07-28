from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from database.database import get_db
from auth.authentication import verify_token
from database.db_user import UserData, UserPlantation


router = APIRouter(
    prefix='/register',
    tags=['register']
)


@router.post('', description='send registration form for verification', response_description="registration form submitted", status_code=status.HTTP_201_CREATED)
def register_user(data: UserData, db: Session = Depends(get_db)):
    return {"message": "User registered successfully", "data" : data.dict()}


@router.post("/plantation", description='send plantation form for verification', response_description="plantation form submitted", status_code=status.HTTP_201_CREATED)
def register_plantation(data: UserPlantation, db: Session = Depends(get_db)):
    return {"message": "Plantation registered successfully", "data" : data.dict()}
