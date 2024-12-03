from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database.database import get_db
from database.db_prediction import fetch_prediction, fetch_all_predictions
from database.db_prediction import PredictionRequest, PredictionResponse
from auth.authentication import verify_token, get_current_user

router = APIRouter(
    prefix='/prediction',
    tags=['prediction']
)

@router.get("/prediction/{plantation_id}/{sensor_id}", response_model=PredictionResponse)
async def get_prediction(sensor_id: int, plantation_id: int,db: Session = Depends(get_db)):
    """
    API endpoint to fetch a single prediction based on sensor_id and plantation_id.
    Args:
    - request: PredictionRequest model containing sensor_id and plantation_id.
    - db: Database session dependency.
    
    Returns:
    - A PredictionResponse model with the prediction data.
    """
    prediction = await fetch_prediction(db, sensor_id)
    return PredictionResponse(
        image_id=prediction.image_id,
        sensor_id=prediction.sensor_id,
        plantation_id=prediction.plantation_id,
        prediction_details=prediction.prediction_details,
        pest=prediction.pest,
        weed=prediction.weed,
        disease=prediction.disease,
        created_at=prediction.created_at,
    )

@router.get("/predictions/{plantation_id}/{sensor_id}", response_model=list[PredictionResponse])
async def get_all_predictions(sensor_id: int, plantation_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to fetch all predictions based on sensor_id and plantation_id.
    Args:
    - sensor_id: Sensor ID to filter
    - plantation_id: Plantation ID to filter
    - db: Database session dependency.
    
    Returns:
    - A list of PredictionResponse models with the predictions data.
    """
    predictions = await fetch_all_predictions(db, sensor_id)
    return [
        PredictionResponse(
            image_id=prediction.image_id,
            sensor_id=prediction.sensor_id,
            plantation_id=prediction.plantation_id,
            prediction_details=prediction.prediction_details,
            pest=prediction.pest,
            weed=prediction.weed,
            disease=prediction.disease,
            created_at=prediction.created_at,
        )
        for prediction in predictions
    ]
