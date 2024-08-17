import uuid
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database.models import DbContact
from fastapi import status, HTTPException


class ContactData(BaseModel):
    first_name: str
    last_name: str
    organization: str
    email: EmailStr
    subject: str
    message: str


def create_contact(db: Session, request: ContactData):
    new_contact = DbContact(
        first_name=request.first_name,
        last_name=request.last_name,
        organization=request.organization,
        email=request.email,
        subject=request.subject,
        message=request.message
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

def get_contact(db: Session, contact_id: int):
    return db.query(DbContact).filter(DbContact.contact_id == contact_id).first()

def get_all_contacts(db: Session):
    return db.query(DbContact).all()
