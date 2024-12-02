from pydantic.types import UUID
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.models import DbSensor, DbSensorImage, DbSensorData
from database.database import supabase
from fastapi import status, HTTPException, UploadFile, File
from datetime import datetime
import time
from pydantic import BaseModel, Field
import uuid


class SensorBase(BaseModel):
    sensor_id: int
    plantation_id: int

class SensorDisplay(BaseModel):
    sensor_id: int
    plantation_id: int

class SensorData(BaseModel):
    sensor_id: int
    temperature: float
    humidity: float
    nh3_level: float
    co2_level: float

# Response Model for Retrieving Image Data
class ImageResponse(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the image record")
    media_url: str = Field(..., description="URL of the image media")
    sensor_id: int = Field(..., description="ID of the sensor")
    plantation_id: int = Field(..., description="ID of the plantation")
    timestamp: datetime = Field(..., description="Timestamp of the image capture")

async def add_sensor(db: Session, request: SensorBase):
    new_sensor = DbSensor(
        sensor_id=request.sensor_id,
        plantation_id=request.plantation_id
    )
    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)
    return new_sensor


async def upload_image(db: Session, file: UploadFile, sensor_id: uuid):
    # Check if the sensor exists
    sensor = db.query(DbSensor).filter(DbSensor.sensor_id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")

    image_content = await file.read()

    file_name = f"{sensor_id}_{int(time.time())}.jpg"

    response = supabase.storage.from_('prediction_imgs').upload(file_name, image_content)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    # Extract the file URL from the response
    file_url = response.json().get('Key')

    if not file_url:
        raise HTTPException(status_code=500, detail="Failed to retrieve file URL from the response")

    # Save the image to the database
    new_image = DbSensorImage(
        media_url=file_url,
        sensor_id=sensor_id,
        plantation_id=sensor.plantation_id,
        created_at=datetime.datetime.now()
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return new_image

# def get_all_images(db: Session):
#     return db.query(DbSensorImage).all()

def get_image(db: Session, image_id: int):
    return db.query(DbSensorImage).filter(DbSensorImage.image_id == image_id).first()

async def add_sensor_data(db: Session, request: SensorData):
    new_data = DbSensorData(
        sensor_id=request.sensor_id,
        temperature=request.temperature,
        humidity=request.humidity,
        nh3_level=request.nh3_level,
        co2_level=request.co2_level
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data