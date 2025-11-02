# app/core/security.py

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings # This line is crucial to import your application settings

# Configuration for password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# JWT Configuration - These values are now fetched from your settings object.
# This ensures that your SECRET_KEY, ALGORITHM, and token expiration times
# are managed centrally via app/core/config.py, which is ideal for production.

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new JWT access token.
    Args:
        data (dict): The payload to encode in the token.
        expires_delta (Optional[timedelta]): Optional timedelta for token expiration.
                                            If None, uses settings.ACCESS_TOKEN_EXPIRE_MINUTES.
    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new JWT refresh token.
    Args:
        data (dict): The payload to encode in the token.
        expires_delta (Optional[timedelta]): Optional timedelta for token expiration.
                                            If None, uses settings.REFRESH_TOKEN_EXPIRE_DAYS.
    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password from the database.
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    # --- DEBUGGING PRINT STATEMENTS START ---
    print(f"DEBUG: Verify - Plain Password Received: '{plain_password}'")
    print(f"DEBUG: Verify - Hashed Password from DB: '{hashed_password}'")
    # --- DEBUGGING PRINT STATEMENTS END ---
    
    is_match = pwd_context.verify(plain_password, hashed_password)
    
    # --- DEBUGGING PRINT STATEMENTS START ---
    print(f"DEBUG: Verify - Password Match Result: {is_match}")
    # --- DEBUGGING PRINT STATEMENTS END ---
    
    return is_match

def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.
    Args:
        password (str): The plain text password.
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)