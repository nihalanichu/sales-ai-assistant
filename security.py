from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from models import User
import jwt

def verify_token(token: str) -> Optional[int]:
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        return payload.get("user_id")
    except:
        return None

# get current user from token and return user object
async def get_current_user(authorization: Optional[str] = Header(None)) -> int:
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")
    
    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization scheme")
    
    current_user_id = verify_token(token)
    if current_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return current_user_id
   