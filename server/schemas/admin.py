from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional


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
    #user_id: uuid.UUID
    name: str
    city: str # location
    createdAt:datetime
    status: str
    class Config:
        from_attributes = True

class PlantationDisplay(BaseModel):
    plantation_id: int
    plantation_name: str
    type: str
    user_name: str
    city: str
    province: str
    country: str
    plantation_width : float
    plantation_length : float
    class Config:
        from_attributes = True




