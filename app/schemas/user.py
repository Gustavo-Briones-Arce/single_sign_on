from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    rut: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_admin: Optional[bool]


class User(UserBase):
    id: str
    on_created: datetime
    on_updated: Optional[datetime]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: Optional[str]


class UserUpdate(UserCreate):
    pass
