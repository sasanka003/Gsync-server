from enum import Enum
from pydantic import BaseModel
import uuid

class Subscription(str, Enum):
    Basic = "Basic"
    Gardener = "Gardener"
    Enterprise = "Enterprise"

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
    subscription: Subscription
    class Config:
        from_attributes = True
