from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from database.database import get_db
from auth.authentication import get_current_user, admin_only
from database import db_plantation 
from database.db_plantation import UserPlantation
from schemas.plantation import PlantationDisplay


router = APIRouter(
    prefix='/plantations',
    tags=['plantation']
)

@router.get("/all", description='get all plantations', response_description="all plantations", response_model=List[PlantationDisplay], responses={404: {"description": "Plantations not found"}})
def get_all_plantations(db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    plantations = db_plantation.get_all_plantations(db)

    response = []
    if plantations:
        for plantation in plantations:
            response.append(PlantationDisplay.model_validate(plantation))
        return response
    
    raise HTTPException(status_code=404, detail="Plantations not found")


@router.post("/register", description='send plantation form for verification', response_description="plantation form submitted", status_code=status.HTTP_201_CREATED)
def register_plantation(data: UserPlantation, db: Session = Depends(get_db)):
    plantation = db_plantation.create_plantation(db, data)
    if plantation:
        return {"message": "Plantation form submitted successfully"}
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="plantation already exist")


@router.get("/{plantation_id}", description='get a plantation by id', response_description="plantation retrieved", response_model=PlantationDisplay, responses={404: {"description": "Plantation not found"}})
def get_plantation(plantation_id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    if token.type != 'SysAdmin':
        try:
            user_plantation = db_plantation.get_user_plantations(db, token.user_id)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You do not have any plantation")
        try:
            plantation = db_plantation.get_plantation(db, plantation_id)
            if plantation and plantation in user_plantation:
                return PlantationDisplay.model_validate(plantation)
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except:
            raise HTTPException(status_code=404, detail="Plantations not found")
    else:
        try:
            plantation = db_plantation.get_plantation(db, plantation_id)
            if plantation:
                return PlantationDisplay.model_validate(plantation)
        except:
            raise HTTPException(status_code=404, detail="Plantations not found")



@router.get("/get/{user_id}", description='get all plantations of a user', response_description="all plantations of a user", response_model=List[PlantationDisplay], responses={404: {"description": "Plantations not found"}})
def get_user_plantations(user_id: uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(get_current_user)): 
    if token.type not in {'SysAdmin', 'EnterpriseAdmin'}:
        if token.user_id == user_id:
            try:
                plantations = db_plantation.get_user_plantations(db, user_id)
                if plantations == None:
                    raise HTTPException(status_code=404, detail="Plantations not found")
                return [PlantationDisplay.model_validate(plantation) for plantation in plantations]
            except ValidationError as e:
                raise HTTPException(status_code=404, detail="Plantations not found")
            except Exception as e:
                raise HTTPException(status_code=404, detail="Plantations not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        try:
            plantations = db_plantation.get_user_plantations(db, user_id)
            if plantations == None:
                raise HTTPException(status_code=404, detail="Plantations not found")
            return [PlantationDisplay.model_validate(plantation) for plantation in plantations]
        except ValidationError as e:
            raise HTTPException(status_code=404, detail="Plantations not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Server error")


@router.delete("/delete/{plantation_id}", description='delete a plantation by id', response_description="plantation deleted", responses={404: {"description": "Plantation not found"}})
def delete_plantation(plantation_id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    plantation_check = db_plantation.get_user_plantations(db, token.user_id)
    count = len(plantation_check)
    if count == 1:
        return {"message": "You can't delete your only plantation"}
    elif count == 0:
        raise HTTPException(status_code=404, detail="Plantations not found")
    if not any(plantation.plantation_id == plantation_id for plantation in plantation_check):
        raise HTTPException(status_code=401, detail="Unauthorised")
    plantation = db_plantation.delete_plantation(db, plantation_id)
    if plantation == 'ok':
        return {"message": "Plantation deleted successfully"}
    raise HTTPException(status_code=404, detail="Plantations not found")


@router.put("/update/{plantation_id}", description='verify a plantation status by id', response_description="plantation updated", responses={404: {"description": "Plantation not found"}})
def update_plantation(plantation_id: int, db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    plantation = db_plantation.update_plantation_status(db, plantation_id)
    if plantation:
        return {"message": "Plantation verified successfully"}
    raise HTTPException(status_code=404, detail="Plantations not found")
