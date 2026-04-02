from datetime import datetime, timedelta, timezone, UTC
from typing import Optional, List
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlmodel import Session, select
from pwdlib import PasswordHash
from app.models.tables import User

# Configuration
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24  # 12 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = PasswordHash.recommended()

# ==================== PASSWORD HANDLING ====================
def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash. Truncate to 72 bytes (bcrypt limit) for consistency."""
    return password_hash.verify(plain_password, hashed_password)

# ==================== JWT TOKEN HANDLING ====================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==================== USER RETRIEVAL ====================
def get_user_from_token(token: str, session: Session):
    """Get user object from JWT token."""
    print("Getting user from token:", token)
    from app.models.tables import User
    payload = decode_token(token)
    user_id = payload.get("sub")
    print("USER ID FROM TOKEN:", user_id)
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

# ==================== DECODE TOKEN ====================
def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    print("compiler reached in decode_token")

    try:
        print("compiler reached in Try statement")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODED PAYLOAD:", payload)
        user_id = payload.get("sub")
        print("USER ID FROM PAYLOAD:", user_id)  
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        payload["sub"] = int(user_id)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )