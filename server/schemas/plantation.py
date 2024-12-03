import datetime
from enum import Enum
from pydantic import BaseModel
from uuid import UUID


class Subscription(str, Enum):
    Basic = "Basic"
    Gardener = "Gardener"
    Enterprise = "Enterprise"

class PlantationStatus(str, Enum):
    Approved = "Approved"
    Unapproved = "Unapproved" 
    Declined = "Declined"

class Plantation_type(str, Enum):
    Indoor = "Indoor"
    Outdoor = "Outdoor"

class Plant_type(str, Enum):
    Tomato = "Tomato"
    Bell_pepper = "Bell_pepper"
    Capsicum = "Capsicum"

class Location(BaseModel):
    city: str
    province: str
    country: str

class Area(BaseModel):
    length: float
    width: float

# create Enum for subscription
class Subscription(str, Enum):
    Basic = "Basic"
    Gardener = "Gardener"
    Enterprise = "Enterprise"

class UserPlantation(BaseModel):
    user_id: UUID
    name: str
    plant_type: Plant_type
    plantation_type: Plantation_type
    city: str
    province: str
    country: str
    area: Area
    subscription: Subscription

class PlantationDisplay(BaseModel):
    plantation_id: int
    name: str
    plant_type: Plant_type
    plantation_type: Plantation_type
    city: str
    province: str
    country: str
    plantation_length: float
    plantation_width: float
    verified: bool
    user_id: UUID
    subscription: Subscription
    class Config:
        from_attributes = True
