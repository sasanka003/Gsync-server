import uuid
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.models import DbPlantation
from fastapi import status, HTTPException


class Location(BaseModel):
    city: str
    province: str
    region: str

class Area(BaseModel):
    length: float
    width: float


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False


class UserPlantation(BaseModel):
    user_id: uuid.UUID
    name: str
    type: str
    location: Location
    area: Area

def create_plantation(db: Session, request: UserPlantation):
    new_plantation = DbPlantation(
        user_id=request.user_id,
        name=request.name,
        type=request.type,
        city=request.location.city,
        province=request.location.province,
        country=request.location.region,
        plantation_length=request.area.length,
        plantation_width=request.area.width
    )
    db.add(new_plantation)
    db.commit()
    db.refresh(new_plantation)
    return new_plantation


def get_plantation(db: Session, plantation_id: int):
    return db.query(DbPlantation).filter(DbPlantation.plantation_id == plantation_id).first()


def get_user_plantations(db: Session, user_id: int):
    return db.query(DbPlantation).filter(DbPlantation.user_id == user_id).all()


def get_user_plantation_count(db: Session, user_id: int):
    return db.query(DbPlantation).filter(DbPlantation.user_id == user_id).count()


def delete_plantation(db: Session, plantation_id: int):
    plantation = db.query(DbPlantation).filter(DbPlantation.plantation_id == plantation_id).first()
    if not plantation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plantation with {plantation_id} not found")

    db.delete(plantation)
    db.commit()
    return 'ok'
