from fastapi import APIRouter, Depends, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from database.database import get_db
from auth.authentication import verify_token, get_current_user
from database import db_plantation 
from database.db_plantation import UserPlantation
from schemas.plantation import PlantationDisplay


router = APIRouter(
    prefix='/plantations',
    tags=['plantation']
)


@router.post("/register", description='send plantation form for verification', response_description="plantation form submitted", status_code=status.HTTP_201_CREATED)
def register_plantation(data: UserPlantation, db: Session = Depends(get_db)):
    plantation = db_plantation.create_plantation(db, data)
    if plantation:
        return {"message": "Plantation form submitted successfully"}
    return status.HTTP_400_BAD_REQUEST


@router.get("/{plantation_id}", description='get a plantation by id', response_description="plantation retrieved", response_model=PlantationDisplay, responses={404: {"description": "Plantation not found"}})
def get_plantation(plantation_id: int, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    plantation = db_plantation.get_plantation(db, plantation_id)
    if plantation:
        return PlantationDisplay.model_validate(plantation)
    return status.HTTP_404_NOT_FOUND


@router.get("/get/{user_id}", description='get all plantations of a user', response_description="all plantations of a user", response_model=List[PlantationDisplay], responses={404: {"description": "Plantations not found"}})
def get_user_plantations(user_id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):   
    try:
        plantations = db_plantation.get_user_plantations(db, user_id)
        if not plantations:
            return status.HTTP_404_NOT_FOUND
        return [PlantationDisplay.model_validate(plantation) for plantation in plantations]
    except ValidationError as e:
        raise status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        raise status.HTTP_500_INTERNAL_SERVER_ERROR


@router.delete("/delete/{plantation_id}", description='delete a plantation by id', response_description="plantation deleted", responses={404: {"description": "Plantation not found"}})
def delete_plantation(plantation_id: int, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    count = db_plantation.get_user_plantation_count(db, token)
    if count == 1:
        return {"message": "You can't delete your only plantation"}
    elif count == 0:
        return status.HTTP_404_NOT_FOUND
    
    plantation = db_plantation.delete_plantation(db, plantation_id)
    if plantation == 'ok':
        return {"message": "Plantation deleted successfully"}
    return status.HTTP_404_NOT_FOUND


@router.put("/update/{plantation_id}", description='verify a plantation status by id', response_description="plantation updated", responses={404: {"description": "Plantation not found"}})
def update_plantation(plantation_id: int, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    plantation = db_plantation.update_plantation_status(db, plantation_id)
    if plantation:
        return {"message": "Plantation verified successfully"}
    return status.HTTP_404_NOT_FOUND


@router.get("/all", description='get all plantations', response_description="all plantations", response_model=List[PlantationDisplay], responses={404: {"description": "Plantations not found"}})
def get_all_plantations(db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    print(token)
    plantations = db_plantation.get_all_plantations(db)

    response = []
    if plantations:
        for plantation in plantations:
            response.append(PlantationDisplay.model_validate(plantation))
        return response
    
    return status.HTTP_404_NOT_FOUND
