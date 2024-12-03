from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from database.models import DbPredictions

# Request model
class PredictionRequest(BaseModel):
    sensor_id: int
    plantation_id: int

# Response model
class PredictionResponse(BaseModel):
    image_id: int
    sensor_id: int
    plantation_id: int
    prediction_details: str
    pest: bool
    weed: bool
    disease: bool
    created_at: datetime


async def fetch_prediction(db: Session, sensor_id: int):
    """
    Fetch a single prediction based on sensor_id and plantation_id.
    Args:
    - db: SQLAlchemy Session
    - sensor_id: Sensor ID to filter
    - plantation_id: Plantation ID to filter
    
    Returns:
    - A single prediction record.
    """
    try:
        prediction = (
            db.query(DbPredictions)
            .filter(DbPredictions.sensor_id == sensor_id)
            .order_by(DbPredictions.created_at.desc())  # Fetch the latest prediction
            .first()
        )

        if not prediction:
            raise NoResultFound(
                f"No prediction found for sensor_id {sensor_id}"
            )

        return prediction
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

async def fetch_all_predictions(db: Session, sensor_id: int):
    """
    Fetch all predictions based on sensor_id and plantation_id.
    Args:
    - db: SQLAlchemy Session
    - sensor_id: Sensor ID to filter
    - plantation_id: Plantation ID to filter
    
    Returns:
    - A list of prediction records.
    """
    predictions = (
        db.query(DbPredictions)
        .filter(DbPredictions.sensor_id == sensor_id)
        .order_by(DbPredictions.created_at.desc())  # Latest predictions first
        .all()
    )

    if not predictions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No predictions found for sensor_id {sensor_id}"
        )

    return predictions
