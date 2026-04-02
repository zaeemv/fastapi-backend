
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.tables import User
from app.schemas import schemas

router = APIRouter()

@router.get("/users/", response_model=List[schemas.UserRead], tags=["users"])
def list_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.exec(select(User).offset(skip).limit(limit)).all()
