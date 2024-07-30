from pydantic import BaseModel

class Contact(BaseModel):
    contact_id: int
    first_name: str
    last_name: str
    organization: str
    email: str
    subject: str
    message: str
    checked: bool
    created_at: str
    class Config:
        from_attributes = True
