from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from auth.authentication import verify_token

router = APIRouter(
    prefix='/posts',
    tags=['posts', 'comments']
)


