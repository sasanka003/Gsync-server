from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import db_sensor, db_plantation
from database.database import get_db
from database.db_sensor import ImageResponse, SensorBase, SensorDisplay, SensorData
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

@router.post('/save_image', description="save camera image from sensor kit", response_model=ImageResponse, deprecated=True)
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

@router.post('/add_data', description="add sensor data", response_model=SensorData, deprecated=True)
async def add_sensor_data(
    request: SensorData,
    db: Session = Depends(get_db)
):
    return await db_sensor.add_sensor_data(db, request)

@router.get('/get_data/{plantation_id}/{sensor_id}', description="get sensor data", response_model=SensorData)
async def get_sensor_data(
    sensor_id: int,
    plantation_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(get_current_user)
):
    user_plantation = db_plantation.get_user_plantations(db, token.user_id)
    if user_plantation.plantation_id!=plantation_id:
        raise HTTPException(
            status_code=400,
            detail="Unauthorized."
        )
    return await db_sensor.get_sensor_data(db, sensor_id, plantation_id)

@router.get("/multiple_data/{plantation_id}/{sensor_id}")
async def fetch_multiple_sensor_data(
    sensor_id: int,
    plantation_id: int,
    time_period: str,
    db: Session = Depends(get_db),
    token: dict = Depends(get_current_user)
):
    """
    Fetch sensor data for multiple sensors within a specified time period.
    Args:
    - sensor_ids: List of sensor IDs to fetch data for.
    - plantation_id: Plantation ID for authorization.
    - time_period: One of ['last_day', 'last_week', 'last_month', 'last_year'].
    """
    user_plantation = db_plantation.get_user_plantations(db, token.user_id)
    if user_plantation.plantation_id!=plantation_id:
        raise HTTPException(
            status_code=400,
            detail="Unauthorized."
        )
    return await db_sensor.get_multiple_sensors_data(db, sensor_id, plantation_id, time_period)