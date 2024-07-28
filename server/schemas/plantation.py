from pydantic import BaseModel

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
    user_id: str
    class Config:
        from_attributes = True
