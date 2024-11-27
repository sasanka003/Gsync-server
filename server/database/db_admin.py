from database.models import DbUser, DbPlantation, DbPlantationStatus, DbPlantationComments, DbHelpRequest
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from sqlalchemy import asc,func
import uuid
from pydantic import BaseModel
from sqlalchemy.orm import aliased

class EditGardener(BaseModel):
    name:str
    email:str
    #address
    phone:str

class Comment(BaseModel):
    plantation_id: int
    comment: str

class UpdatePlantationStatus(BaseModel):
    plantation_width: float
    plantation_length: float
    comment: str
    is_approved: bool

class HelpRequestComment(BaseModel):
    comment: str



def get_all_gardeners(db: Session, page:int, page_size:int):
    offset = (page - 1) * page_size

    gardeners = db.query(DbUser.user_id, DbUser.name, DbUser.email, DbUser.phone).filter(DbUser.type == 'User').order_by(asc(DbUser.created_at)).offset(offset).limit(page_size).all()
    return gardeners

def delete_gardener(db: Session,user_id: uuid.UUID):
    gardener = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not gardener:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardener not found")

    db.delete(gardener)
    db.commit()
    return 'ok'

def edit_gardener(db: Session, user_id: uuid.UUID, request:EditGardener):
    gardener = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not gardener:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardener not found")

    gardener.name = request.name
    gardener.email = request.email
    gardener.phone = request.phone

    db.commit()
    db.refresh(gardener)

    return gardener

# Get all plantation requests
def get_all_plantations(db: Session):

    result = db.query(DbPlantation.plantation_id, DbPlantation.type, DbUser.name, DbPlantation.city, DbPlantation.createdAt, DbPlantationStatus.status) \
        .join(DbPlantationStatus,DbPlantation.plantation_id == DbPlantationStatus.plantation_id) \
        .join(DbUser, DbPlantation.user_id == DbUser.user_id) \
        .all()
    return result

def get_plantation(db: Session, plantation_id: int):
    user_alias = aliased(DbUser)  # Alias for clarity
    return db.query(
        DbPlantation.plantation_id,
        DbPlantation.name.label("plantation_name"),  # Alias for plantation name
        DbPlantation.type,
        user_alias.name.label("user_name"),  # Alias for user name
        DbPlantation.city,
        DbPlantation.province,
        DbPlantation.country,
        DbPlantation.plantation_width,
        DbPlantation.plantation_length
    ) \
        .join(DbUser, DbPlantation.user_id == DbUser.user_id)\
        .filter(DbPlantation.plantation_id == plantation_id)\
        .first()


def update_plantation_status(db: Session, plantation_id: int, request:UpdatePlantationStatus):

    # Fetch the plantation
    plantation = db.query(DbPlantation).filter(DbPlantation.plantation_id == plantation_id).first()

    if not plantation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plantation not found")

    # Update plantation dimension
    plantation.plantation_width = request.plantation_width
    plantation.plantation_length = request.plantation_length

    # Fetch the latest status entry for the plantation
    latest_status_entry = db.query(DbPlantationStatus) \
        .filter(DbPlantationStatus.plantation_id == plantation_id) \
        .order_by(DbPlantationStatus.updated_at.desc()) \
        .first()

    if not latest_status_entry:
        # If no status exists, create a new one
        status = DbPlantationStatus(
            plantation_id=plantation.plantation_id,
            status="Approved" if request.is_approved else "Unapproved"
        )
        db.add(status)
    else:
        # Update the existing status
        latest_status_entry.status = "Approved" if request.is_approved else "Unapproved"
        latest_status_entry.updated_at = func.now()

    # Add a comment
    if request.comment:
        plantation_comment = DbPlantationComments(
            plantation_id=plantation_id,
            comment=request.comment
        )
        db.add(plantation_comment)

    # Commit the changes
    db.commit()
    db.refresh(plantation)
    return plantation


def add_comment(db:Session, request:Comment):
    new_comment = DbPlantationComments (
        plantation_id = request.plantation_id,
        comment = request.comment
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all_help_requests(db:Session):
    result = db.query(
        DbHelpRequest.help_request_id,
        DbHelpRequest.subject,
        DbHelpRequest.message,
        DbHelpRequest.createdAt,
        DbUser.name,
        DbUser.type
    ) \
    .join(DbUser,DbHelpRequest.user_id == DbUser.user_id) \
    .all()
    return result

def get_help_request(db:Session, help_request_id:int):
    result = db.query(
        DbHelpRequest.help_request_id,
        DbHelpRequest.subject,
        DbHelpRequest.message,
        DbHelpRequest.createdAt,
        DbUser.name,
        DbUser.type
    ) \
        .join(DbUser, DbHelpRequest.user_id == DbUser.user_id) \
        .filter(DbHelpRequest.help_request_id == help_request_id) \
        .first()
    return result

def add_comment(db:Session, help_request_id:int, request:HelpRequestComment):

    help_request = db.query(DbHelpRequest).filter(DbHelpRequest.help_request_id == help_request_id).one()

    if not help_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Help request not found")

    help_request.comment = request.comment

    db.commit()
    db.refresh(help_request)
    return help_request