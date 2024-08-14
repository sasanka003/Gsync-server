from database.models import DbUser
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from sqlalchemy import asc


def get_all_gardeners(db: Session, page:int, page_size:int):

    offset = (page - 1) * page_size

    gardeners = db.query(DbUser).filter(DbUser.type == 'User').order_by(asc(DbUser.created_at)).offset(offset).limit(page_size).all()

    return gardeners