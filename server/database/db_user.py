import uuid
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.models import DbUser
from fastapi import status, HTTPException


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False



