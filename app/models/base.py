from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class CustomerCommon(SQLModel):
    name: str
    contact_info: Optional[str] = None

class CustomerBase(CustomerCommon):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCommon(SQLModel):    
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True

class UserBase(UserCommon):
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))