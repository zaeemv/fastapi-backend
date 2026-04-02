from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel

from app.models.base import CustomerBase, UserBase

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None

class TokenResponse(SQLModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None