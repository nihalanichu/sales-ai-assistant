# import authentication router
from fastapi import APIRouter, Depends, HTTPException, status
from docs.schemas import UserSignup, UserLogin
from sqlalchemy.orm import Session
from docs.models import User
from docs.database import get_db
from docs.security import hash_password, get_current_user, verify_password, generate_token

authentication_router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@authentication_router.post("/signup")
async def signup(request: UserSignup, db: Session = Depends(get_db)):
    hashed_password = hash_password(request.password)
    print("Hashed password:", hashed_password)
    existing_user = db.query(User).filter(User.email == request.email).first()
    

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = User(
        email=request.email,
        full_name=request.full_name,
        password=request.password
    )
    db.add(new_user)
    db.commit()
    return {"status": "success", "code": 200, "message": "user created successfully"}

@authentication_router.post("/login")
async def login(request: UserLogin, db: Session = Depends(get_db)):    
    existing_user = db.query(User).filter(User.email == request.email).first()
    if not existing_user or existing_user.password != request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    # generate token
    token = get_current_user(existing_user.id)
    return {"message": "Login successful", "token": token}