from pydantic import BaseModel
import uuid

class GradenersDisplay(BaseModel):
    user_id: uuid.UUID
    name: str
    email: str
    # phone: str
    class Config:
        from_attributes = True
