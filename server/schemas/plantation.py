from pydantic import BaseModel
import uuid

class PlantationDisplay(BaseModel):
    plantation_id: int
    name: str
    type: str
    city: str
    province: str
    country: str
    plantation_length: float
    plantation_width: float
    verified: bool
    user_id: uuid.UUID
    class Config:
        from_attributes = True
