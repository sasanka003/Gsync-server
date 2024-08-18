from database.models import DbUser, DbPlantation, DbPlantationStatus
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from sqlalchemy import asc,func
import uuid



def get_all_gardeners(db: Session, page:int, page_size:int):

    offset = (page - 1) * page_size

    gardeners = db.query(DbUser).filter(DbUser.type == 'User').order_by(asc(DbUser.created_at)).offset(offset).limit(page_size).all()

    return gardeners

def delete_gardener(db: Session,user_id: uuid.UUID):
    gardener = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if not gardener:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardener not found")

    db.delete(gardener)
    db.commit()
    return 'ok'


def get_all_plantations(db: Session):

    result = db.query(DbPlantation.plantation_id, DbPlantation.type, DbPlantation.user_id, DbPlantation.city, DbPlantation.createdAt, DbPlantationStatus.status) \
        .join(DbPlantationStatus,DbPlantation.plantation_id == DbPlantationStatus.plantation_id).all()
    return result


def update_plantation_status(db: Session, plantation_id: int, status: str):

    # Fetch the plantation
    plantation = db.query(DbPlantation).filter(DbPlantation.plantation_id == plantation_id).first()

    if not plantation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plantation not found")

    # Fetch the latest status entry for the plantation
    latest_status_entry = db.query(DbPlantationStatus) \
        .filter(DbPlantationStatus.plantation_id == plantation_id) \
        .order_by(DbPlantationStatus.updated_at.desc()) \
        .first()

    if latest_status_entry:
        # Update the status if it exists
        latest_status_entry.status = status
        latest_status_entry.updated_at = func.now()
        db.commit()
        db.refresh(latest_status_entry)
        return latest_status_entry
    else:
        # Create a new status entry if none exists
        status_entry = DbPlantationStatus(
            plantation_id=plantation.plantation_id,
            status=status,
        )
        db.add(status_entry)
        db.commit()
        db.refresh(status_entry)
        return status_entry

