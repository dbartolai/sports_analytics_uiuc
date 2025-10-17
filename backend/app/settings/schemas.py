from pydantic import BaseModel
from datetime import datetime

class UserSettingsBase(BaseModel):
    user_id: str
    theme: str = "light"
    notifications: bool = True
    dashboard_layout: str = "compact"

class UserSettingsResponse(UserSettingsBase):
    created_at: datetime
    updated_at: datetime