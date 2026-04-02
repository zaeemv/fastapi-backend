from .base import *
from typing import Optional
from sqlmodel import Field

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)