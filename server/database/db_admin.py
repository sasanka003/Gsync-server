from database.models import DbUser, DbPlantation, DbPlantationStatus
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from sqlalchemy import asc


def get_all_gardeners(db: Session, page:int, page_size:int):

    offset = (page - 1) * page_size

    gardeners = db.query(DbUser).filter(DbUser.type == 'User').order_by(asc(DbUser.created_at)).offset(offset).limit(page_size).all()

    return gardeners

def get_all_plantations(db: Session):
    return db.query(DbPlantation).all()


def update_plantation_status(db: Session, plantation_id: int, status: str):

    # Fetch the plantation
    plantation = db.query(DbPlantation).filter(DbPlantation.plantation_id == plantation_id).first()

    if not plantation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plantation not found")

    status_entry = DbPlantationStatus(
        plantation_id=plantation.plantation_id,
        status=status,
    )
    db.add(status_entry)
    db.commit()
    db.refresh(status_entry)
    return status_entry
