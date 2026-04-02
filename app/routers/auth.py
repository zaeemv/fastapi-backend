from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.auth import get_user_from_token, verify_password, create_access_token, hash_password
from app.database import get_session
from app.schemas import schemas
from app.models.tables import User
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """Dependency to get current authenticated user from token."""
    print("TOKEN RECEIVED:", token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    
    user = get_user_from_token(token, session)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive",
        )
    
    return user

@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Login endpoint. Returns JWT token with user info and permissions."""
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    print("USER FOUND:", user)
    if not user or not verify_password(form_data.password, user.password or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )

    
    """Create JWT access Token"""

    token_data = {
        "sub": str(user.id),
        "username": user.username,
    }
    access_token = create_access_token(data=token_data, expires_delta=timedelta(days=30))
    
    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        email=user.email,
    )

@router.post("/register", response_model=schemas.UserRead)
def register(
    user_data: schemas.UserCreate, 
    session: Session = Depends(get_session)
    ):
    """Register a new user. New users get the 'Viewer' role by default."""
    existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        is_active=True,
        password=hashed_password
    )
    print("REGISTERING USER:", db_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user