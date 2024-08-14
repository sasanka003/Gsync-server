from fastapi import APIRouter, Depends, status,Query
from typing import Optional, List
from database.database import get_db
from database import db_admin
from schemas.admin import GradenersDisplay
from auth.authentication import verify_token, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.get("/gardeners/", description='get all gardeners', response_description="all gardeners", response_model=List[GradenersDisplay], responses={404: {"description": "Gardeners not found"}})
def get_all_gardeners(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1),db: Session = Depends(get_db)): #token: dict = Depends(get_current_user)
    gardeners = db_admin.get_all_gardeners(db, page,page_size)

    response = []
    if gardeners:
        for gardener in gardeners:
            response.append(GradenersDisplay.model_validate(gardener))
        return response

    return status.HTTP_404_NOT_FOUND
