from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jose.exceptions import JWTError
from database.database import get_db, supabase
import json

from database.models import DbUser


security = HTTPBearer()



async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user = supabase.auth.get_user(token).model_dump_json()
        return json.loads(user)
    except JWTError | json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: dict = Depends(verify_token), db: Session = Depends(get_db)):
    user = token.get('user')
    user_id = user.get('id')
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid token payload")
    user = db.query(DbUser).filter(DbUser.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_id


async def admin_only(current_user: dict = Depends(get_current_user)):
    if current_user.type != 'SysAdmin':
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user
