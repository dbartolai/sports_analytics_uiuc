from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserProfileBase(BaseModel):
    user_id: str
    email: EmailStr
    display_name: str
    avatar_url: str

class UserProfileResponse(UserProfileBase):
    join_date: datetime
    created_at: datetime
    updated_at: datetime