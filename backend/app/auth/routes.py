from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from . import utils, models
from .models import User  # Create a User model

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: models.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists in database
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user in database
    hashed_password = utils.hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"msg": "User registered succeessfully", "user_id": db_user.id}

@router.post("/login", response_model=models.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW_Authenticate": "Bearer"}
        )
    
    token = utils.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}