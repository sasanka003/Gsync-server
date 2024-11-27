import uuid
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.models import DbUser,DbHelpRequest
from fastapi import status, HTTPException
from sqlalchemy import func
import uuid


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False

class HelpRequest(BaseModel):
    subject:str
    message:str

def create_help_request(db: Session, user_id:uuid.UUID, request:HelpRequest):
    new_help_request = DbHelpRequest(
        user_id = user_id,
        subject = request.subject,
        message= request.message,
        createdAt = func.now()
    )
    db.add(new_help_request)
    db.commit()
    db.refresh(new_help_request)
    return new_help_request

