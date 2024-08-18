from fastapi import APIRouter, Depends, status,Query,HTTPException
from typing import Optional, List
from database.database import get_db
from database import db_admin, db_plantation
from schemas.admin import GradenersDisplay, PlantationDisplay
from auth.authentication import verify_token, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.get("/gardeners/", description='get all gardeners', response_description="all gardeners", response_model=List[GradenersDisplay], responses={404: {"description": "Gardeners not found"}})
def get_all_gardeners(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    gardeners = db_admin.get_all_gardeners(db, page,page_size)

    response = []
    if gardeners:
        for gardener in gardeners:
            response.append(GradenersDisplay.model_validate(gardener))
        return response

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gardeneres not found")

@router.get("/plantations", description='get all plantations', response_description="all plantations", response_model=List[PlantationDisplay], responses={404: {"description": "Plantations not found"}})
def get_all_plantations(db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    plantations = db_admin.get_all_plantations(db)

    response = []
    if plantations:
        for plantation in plantations:
            response.append(PlantationDisplay.model_validate(plantation))
        return response

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plantation not found")

@router.put("/plantations/{plantation_id}/{status}", description='update plantation status', response_description="plantation status updated", responses={404: {"description": "Plantation not found"}})
def update_plantation_status(plantation_id: int, status: str, db: Session = Depends(get_db)): #token: dict = Depends(get_current_user)
    if status not in ['Unapproved', 'Approved', 'Declined']:
        raise HTTPException(status_code=400, detail="Invalid status")

    plantation_status = db_admin.update_plantation_status(db, plantation_id, status)
    if plantation_status:
        return {"message": "Plantation status updated successfully"}
    return status.HTTP_404_NOT_FOUND