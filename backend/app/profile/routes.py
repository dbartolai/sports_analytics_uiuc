from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from . import models, schemas

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("", response_model=schemas.UserProfileResponse)
def get_user_profile(userID: str, db: Session = Depends(get_db)):
    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == userID).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    return profile