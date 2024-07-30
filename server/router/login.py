from fastapi import APIRouter, Depends, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class LoginData(BaseModel):
    email: EmailStr
    password: str

class RegistrationData(BaseModel):
    email: EmailStr
    password: str


router = APIRouter(
    prefix='/auth',
    tags=['test']
)


# login routes for testing
@router.post("/login")
async def login(login_data: LoginData):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": login_data.email,
            "password": login_data.password
        })
        return {"access_token": response.session.access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register")
async def register(registration_data: RegistrationData):
    try:
        response = supabase.auth.sign_up({
            "email": registration_data.email,
            "password": registration_data.password
        })
        return {"user_id": response.user.id, "email": response.user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    