from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from database import db_votes
from database.database import get_db

router = APIRouter(
    prefix='/votes',
    tag=['votes']
)

