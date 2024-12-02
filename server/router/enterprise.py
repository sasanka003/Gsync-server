from fastapi import APIRouter, Depends, status, Query, HTTPException
from typing import List
from database.database import get_db
from database import db_admin
from schemas.admin import GardenersDisplay
from auth.authentication import verify_token, get_current_user
from sqlalchemy.orm import Session
import uuid
from database.db_admin import EditGardener

router = APIRouter(
    prefix='/enterprise/admin',
    tags=['admin', 'enterprise', 'user']
)


@router.get("/gardeners/", description='get all gardeners for the enterprise', response_description="all gardeners registered under enterprise", response_model=List[GardenersDisplay], responses={404: {"description": "Gardeners not found"}})
def get_all_gardeners(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    gardeners = db_admin.get_all_gardeners(db, page,page_size)

    response = []
    if gardeners:
        for gardener in gardeners:
            response.append(GardenersDisplay.model_validate(gardener))
        return response

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardeners not found")

@router.delete("/gardener/{user_id}", description='delete a gardener', response_description="gardener deleted",responses={404: {"description": "Gardener not found"}})
def remove_gardener(user_id:uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    gardener = db_admin.delete_gardener(db, user_id)
    if gardener == 'ok':
        return {"message": "Gardener deleted successfully"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardener not found")


@router.put("/gardener/{user_id}", description='edit a gardner', response_description="gardener edited", responses={404: {"description": "Gardener not found"}})
def edit_gardener(user_id:uuid.UUID, request:EditGardener, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    gardener = db_admin.edit_gardener(db, user_id, request)
    if gardener:
        return {"message": "Gardener edited successfully"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardener not found")
