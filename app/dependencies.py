# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os
import sys
import logging

from passlib.context import CryptContext


# Configure logging for this module
logger = logging.getLogger(__name__)
# IMPORTANT: Set logging level back to INFO for normal operations
logging.basicConfig(level=logging.INFO)

# Internal imports
from app.database import get_db
from app.models.user import User # Import the User model

# Load environment variables for JWT secret key
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# --- Password Hashing Utilities ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- JWT Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Default token expiration

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
bearer_scheme = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# get_current_user now uses HTTPBearer to extract the token
async def get_current_user(security: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    # Reverted to INFO level, so these DEBUG logs won't appear unless logging level is changed externally
    logger.debug("DEBUG: get_current_user entered.")

    if not security or not security.credentials:
        logger.error("No token credentials found in security object.") # Changed to INFO, will appear if level is INFO or lower
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = security.credentials
    logger.debug(f"Token received (first 10 chars): {token[:10]}...")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug("Attempting JWT decode.")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT decode successful. Payload: {payload}")

        username: str = payload.get("sub")
        logger.debug(f"Extracted username (sub): {username}")

        if username is None:
            logger.warning("'sub' (username) not found in JWT payload.")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWT decoding error: {e}", exc_info=True)
        raise credentials_exception
    except Exception as e:
        logger.error(f"An unexpected error occurred during token processing: {e}", exc_info=True)
        raise credentials_exception

    logger.debug(f"Looking up user by username: {username}")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.warning(f"User '{username}' not found in database.")
        raise credentials_exception

    logger.debug(f"User '{user.username}' found. Checking if active.")
    if not user.is_active:
        logger.warning(f"User '{user.username}' is inactive.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please contact support.",
        )

    logger.debug(f"User '{user.username}' is active and authenticated.")
    return user
