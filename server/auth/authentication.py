import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jose.exceptions import JWTError
from jose import jwt
from database.database import get_db
from dotenv import load_dotenv

from database.models import DbUser

load_dotenv()

security = HTTPBearer()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = token.get('sub')
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid token payload")
    user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
