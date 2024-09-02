from fastapi import APIRouter, Depends, status,Query,HTTPException
from typing import Optional, List
from database.database import get_db
from database import db_admin, db_plantation
from schemas.admin import GardenersDisplay, PlantationDisplay, PlantationRequestDisplay
from auth.authentication import admin_only
from sqlalchemy.orm import Session
import uuid
from database.db_admin import EditGardener, Comment

router = APIRouter(
    prefix='/main/admin',
    tags=['admin']
)

@router.get("/gardeners/", description='get all gardeners', response_description="all gardeners", response_model=List[GardenersDisplay], responses={404: {"description": "Gardeners not found"}})
def get_all_gardeners(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),db: Session = Depends(get_db), token: dict = Depends(admin_only)):

    gardeners = db_admin.get_all_gardeners(db, page,page_size)

    response = []
    if gardeners:
        for gardener in gardeners:
            response.append(GardenersDisplay.model_validate(gardener))
        return response

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardeners not found")


@router.delete("/gardener/{user_id}", description='delete a gardener', response_description="gardener deleted",responses={404: {"description": "Gardener not found"}})
def remove_gardener(user_id:uuid.UUID, db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    if user_id == token.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete yourself")
    gardener = db_admin.delete_gardener(db,user_id)
    if gardener == 'ok':
        return {"message": "Gardener deleted successfully"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardener not found")


@router.put("/gardener/{user_id}", description='edit a gardner', response_description="gardener edited", responses={404: {"description": "Gardener not found"}}, deprecated=True)
def edit_gardener(user_id:uuid.UUID, request:EditGardener, db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    gardener = db_admin.edit_gardener(db,user_id,request)
    if gardener:
        return {"message": "Gardener edited successfully"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardener not found")


# Get all plantation requests
@router.get("/plantations", description='get all plantations', response_description="all plantations", response_model=List[PlantationRequestDisplay], responses={404: {"description": "Plantations not found"}})
def get_all_plantations(db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    plantations = db_admin.get_all_plantations(db)

    response = []
    if plantations:
        for plantation in plantations:
            response.append(PlantationRequestDisplay.model_validate(plantation))
        return response

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plantation not found")

@router.get("/plantation/{plantation_id}", description='get a plantation by id', response_description="plantation retrieved", response_model=PlantationDisplay, responses={404: {"description": "Plantation not found"}})
def get_plantation(plantation_id: int, db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    plantation = db_admin.get_plantation(db, plantation_id)
    if plantation:
        return PlantationDisplay.model_validate(plantation)
    return status.HTTP_404_NOT_FOUND

@router.put("/plantations/{plantation_id}/{status}", description='update plantation status', response_description="plantation status updated", responses={404: {"description": "Plantation not found"}})
def update_plantation_status(plantation_id: int, status: str, db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    if status not in ['Unapproved', 'Approved', 'Declined']:
        raise HTTPException(status_code=400, detail="Invalid status")

    plantation_status = db_admin.update_plantation_status(db, plantation_id, status)
    if plantation_status:
        return {"message": "Plantation status updated successfully"}
    return status.HTTP_404_NOT_FOUND

@router.post("/comment", description='add comment for plantation', response_description="add comment", status_code=status.HTTP_201_CREATED)
def add_comment(data: Comment, db: Session = Depends(get_db), token: dict = Depends(admin_only)):
    comment = db_admin.add_comment(db,data)
    if comment:
        return {"message": "Comment added successfully"}
    return status.HTTP_400_BAD_REQUEST
