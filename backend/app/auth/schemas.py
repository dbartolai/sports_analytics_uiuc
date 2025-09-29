from sqlalchemy import BaseModel 

class UserCreate(BaseModel):
    email: str
    password: str


