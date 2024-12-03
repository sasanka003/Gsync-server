from sqlalchemy.exc import NoResultFound, MultipleResultsFound, SQLAlchemyError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from database.models import DbSensor, DbSensorImage, DbSensorData, DbPlantation
from database.database import supabase
from fastapi import status, HTTPException, UploadFile, File
from datetime import datetime, timedelta
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

class SensorDataDisplay(BaseModel):
    sensor_id: int
    temperature: float
    humidity: float
    nh3_level: float
    co2_level: float
    created_at: datetime
    image_url: str

# Response Model for Retrieving Image Data
class ImageResponse(BaseModel):
    image_id: int = Field(..., description="Unique identifier of the image record")
    image_url: str = Field(..., description="URL of the image media")
    sensor_id: int = Field(..., description="ID of the sensor")
    plantation_id: int = Field(..., description="ID of the plantation")
    created_at: datetime = Field(..., description="Timestamp of the image capture")

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
        image_url=file_url,
        sensor_id=sensor_id,
        plantation_id=sensor.plantation_id,
        created_at=datetime.now()
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    return new_image

# def get_all_images(db: Session):
#     return db.query(DbSensorImage).all()

def get_image(db: Session, image_id: int):
    try:
        item = db.query(DbSensorImage).filter(DbSensorImage.image_id == image_id).first()
        if item is None:
            raise NoResultFound(f"No result found for image id {image_id}")
        return item 
    except NoResultFound as e:
        print(f"Error: {e}")
    except MultipleResultsFound as e:
        print(f"Error: More than one result found for ID {image_id}")
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
    return None

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


async def get_sensor_data(db: Session, sensor_id: int, plantation_id: int):
    try:
        sensor = db.query(DbSensor).filter(DbSensor.sensor_id == sensor_id).first()
        if sensor is None:
            raise NoResultFound(f"No result found for sensor id {sensor_id}")
        if sensor.plantation_id != plantation_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access to sensor data")
        
        response = db.query(DbSensorData).filter(DbSensorData.sensor_id == sensor_id).order_by(desc(DbSensorData.created_at)).first()
        if response is None:
            raise NoResultFound(f"No result found for sensor id {sensor_id}")
        return response
    except NoResultFound as e:
        print(f"Error: {e}")
    except MultipleResultsFound as e:
        print(f"Error: More than one result found for sensor ID {sensor_id}")
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
    return None

async def get_multiple_sensors_data(db: Session, sensor_id: int, plantation_id: int, time_period: str, limit: int = 10, offset: int = 0):
    try:
        # Define time boundaries based on the requested period
        now = datetime.utcnow()
        if time_period == "last_day":
            start_time = now - timedelta(days=1)
        elif time_period == "last_week":
            start_time = now - timedelta(weeks=1)
        elif time_period == "last_month":
            start_time = now - timedelta(days=30)
        elif time_period == "last_year":
            start_time = now - timedelta(days=365)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid time period")

        # Filter sensors
        sensor = db.query(DbSensor).filter(DbSensor.sensor_id == sensor_id).first()
        if not sensor:
            raise NoResultFound("Sensors not found for the sensor id {sensor_id}")

        # Verify plantation ID
        if sensor.plantation_id != plantation_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unauthorized access to sensor ID {sensor.sensor_id}"
            )

        # Query sensor data within the time period
        sensor_data = (
            db.query(DbSensorData)
            .filter(
                and_(
                    DbSensorData.sensor_id == sensor_id,
                    DbSensorData.created_at >= start_time,
                )
            )
            .order_by(DbSensorData.created_at.desc())
            .limit(limit).offset(offset).all()
        )

        if not sensor_data:
            raise NoResultFound("No data found for the provided sensors and time period")

        return sensor_data

    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))