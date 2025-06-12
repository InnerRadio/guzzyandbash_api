# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os

# Internal Imports
from .database import get_db # To get the database session
from .models.user import User # To type hint current_user

# --- Password Hashing Utilities ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- JWT Configuration (for authentication) ---
SECRET_KEY = os.getenv("SECRET_KEY", "0c5c0d9e5a6145bbf6f6b1bf3382ad6dd1074945657d8bc32102ab460f7bd0d")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- OAuth2 for Authentication ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

# Function to get the current active user from the token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    # --- DEBUGGING PRINTS ---
    print(f"\n--- DEBUG: Inside get_current_user ---")
    print(f"User object found: {user}")
    if user:
        print(f"Type of user object: {type(user)}")
        print(f"User object attributes (user.__dict__): {user.__dict__}")
        print(f"Does 'is_active' attribute exist? {'is_active' in user.__dict__}")
        try:
            print(f"Value of user.is_active: {user.is_active}")
        except AttributeError as e:
            print(f"AttributeError when accessing user.is_active: {e}")
    print(f"--- END DEBUG ---\n")
    # --- END DEBUGGING PRINTS ---

    if user is None or not user.is_active: # This is the line where AttributeError occurs
        raise credentials_exception
    return user