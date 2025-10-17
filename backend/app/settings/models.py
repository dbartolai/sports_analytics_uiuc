from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    theme = Column(String, default="light")
    notifications = Column(Boolean, default=True)
    dashboard_layout = Column(String, default="compact")
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))