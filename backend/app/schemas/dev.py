from pydantic import BaseModel

class DevCreate(BaseModel):
    name: str
    major: str
    grad_year: int
    fun_fact: str | None = None

class DevOut(BaseModel):
    id: int
    name: str
    major: str
    grad_year: int
    fun_fact: str | None

    class Config:
        from_attributes = True  

class DevUpdate(BaseModel):
    name: str | None = None
    major: str | None = None
    grad_year: int | None = None
    fun_fact: str | None = None

