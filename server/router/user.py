from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_mail import MessageSchema
from sqlalchemy.orm import Session

from database.database import get_db
from database import db_user
from auth.authentication import verify_token
from database.db_contact import ContactData
from services.mail_service import fm, MAIL_TO
from database.db_user import HelpRequest
from database import db_user
import uuid

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get("/{user_id}")
async def get_user_profile(user_id: str, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    return {"message": "User profile retrieved successfully"}

@router.post("/contact", description='send contact form', response_description="contact form submitted")
async def contact_us(background_tasks: BackgroundTasks, contact: ContactData, db: Session = Depends(get_db)):
    db_user.create_contact(db, contact)
    message = MessageSchema(
        subject="GSYNC Contact Form",
        recipients=[MAIL_TO],
        template_body=ContactData.model_dump(),
        subtype="html"
    )
    background_tasks.add_task(fm.send_message, message, template_name="contact_email.html")
    return {"message": "Contact form submitted successfully"}


@router.post("/help/{user_id}", description='submit help request', response_description='help request submitted')
def submit_help_request(user_id:uuid.UUID, request:HelpRequest, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    helpRequest = db_user.create_help_request(db, user_id, request)
    if helpRequest:
        return {"message": "Help request submitted successfully"}
    return status.HTTP_400_BAD_REQUEST