from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import Optional
from database import db_sensor
from database.database import get_db
from database.db_sensor import ImageResponse, SensorBase, SensorDisplay
from auth.authentication import verify_token, get_current_user

router = APIRouter(
    prefix='/sensor',
    tags=['sensor']
)

@router.post('/add', description="add a new sensor", response_model=SensorDisplay)
async def add_sensor(
    request: SensorBase,
    db: Session = Depends(get_db)
):
    return await db_sensor.add_sensor(db, request)

@router.post('/save_image', description="save camera image from sensor kit", response_model=ImageResponse)
async def upload_sensor_image(
    file: UploadFile = File(...),
    sensor_id: int = Form(...),
    db: Session = Depends(get_db)
):
    return await db_sensor.upload_image(db, file, sensor_id)

@router.get('/get_image/{image_id}', response_model=ImageResponse)
async def get_sensor_image(image_id: int, db: Session = Depends(get_db)):
    item = db_sensor.get_image(db, image_id)
    if item == None:
        raise status.HTTP_404_NOT_FOUND
    return item