from pydantic import BaseModel
import uuid
from datetime import datetime

class GardenersDisplay(BaseModel):
    user_id: uuid.UUID
    name: str
    email: str
    phone: str | None
    class Config:
        from_attributes = True

class PlantationRequestDisplay(BaseModel):
    plantation_id: int
    type:str
    user_id: uuid.UUID
    city: str # location
    createdAt:datetime
    status: str
    class Config:
        from_attributes = True

class PlantationDisplay(BaseModel):
    plantation_id: int
    user_id: uuid.UUID
    type: str
    #plant_type
    city: str
    #street_name
    #district
    plantation_length : float
    plantation_width : float
    #comments
    class Config:
        from_attributes = True




