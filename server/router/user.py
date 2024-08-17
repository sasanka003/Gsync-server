from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi_mail import MessageSchema
from sqlalchemy.orm import Session

from database.database import get_db
from database import db_user
from auth.authentication import verify_token
from server.database.db_contact import ContactData
from services.mail_service import fm, MAIL_TO


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
