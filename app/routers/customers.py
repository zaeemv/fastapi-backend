from typing import List
from fastapi import APIRouter, Depends
from app.routers.auth import get_current_user
from app.schemas import schemas
from app.database import get_session
from app.models.tables import Customer, User
from sqlmodel import Session, select
router = APIRouter()

@router.post("/customers/", response_model=schemas.CustomerRead, tags=["customers"], )
def create_customer(customer: schemas.CustomerCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_customer = Customer(**customer.model_dump())
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

@router.get("/customers/", response_model=List[schemas.CustomerRead], tags=["customers"])
def list_customers(skip: int = 0, limit: int = 100, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return session.exec(select(Customer).offset(skip).limit(limit)).all()