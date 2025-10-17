from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from . import models, schemas

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("", response_model=schemas.UserSettingsResponse)
def get_user_settings(userID: str, db: Session = Depends(get_db)):
    settings = db.query(models.UserSettings).filter(models.UserSettings.user_id == userID).first()
    
    if not settings:
        return schemas.UserSettingsResponse(
            user_id=userID,
            theme="light",
            notifications=True,
            dashboard_layout="compact"
        )
    
    return settings