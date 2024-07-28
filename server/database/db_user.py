from pydantic import BaseModel


class Location(BaseModel):
    city: str
    province: str
    region: str

class Area(BaseModel):
    length: float
    width: float


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False


class UserPlantation(BaseModel):
    name: str
    type: str
    location: Location
    area: Area

