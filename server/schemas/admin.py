from pydantic import BaseModel
import uuid

class GradenersDisplay(BaseModel):
    user_id: uuid.UUID
    name: str
    email: str
    phone: str
    class Config:
        from_attributes = True

class PlantationDisplay(BaseModel):
    plantation_id: int
    type:str
    user_id: uuid.UUID
    city: str # address
    createdAt:str
    status: str
