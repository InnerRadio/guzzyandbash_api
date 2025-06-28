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
# REVERTED: Set logging level back to INFO for production, or DEBUG if desired for general debugging
logging.basicConfig(level=logging.INFO) # Changed back to INFO for less verbose output

# Internal imports
from app.database import get_db
from app.models.user import User # Import the User model
from app.schemas.user_schemas import UserRole # Import UserRole from schemas

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
# REVERTED: Load SECRET_KEY from environment variable for security
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Default token expiration

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")
# REMOVED: Temporary FULL SECRET_KEY logging for security
logger.info("SECRET_KEY loaded successfully from environment (masked for security).")

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
    logger.debug(f"DEBUG: Token created. Payload exp: {expire.isoformat()}") # This logging level is DEBUG
    return encoded_jwt

async def get_current_user(security: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    logger.debug("DEBUG: get_current_user entered.") # This logging level is DEBUG

    if not security or not security.credentials:
        logger.error("DEBUG: No token credentials found in security object.") # This logging level is DEBUG
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = security.credentials
    logger.debug(f"DEBUG: Full token received: {token}") # This logging level is DEBUG

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug("DEBUG: Attempting JWT decode.") # This logging level is DEBUG
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"DEBUG: JWT decode successful. Payload: {payload}") # This logging level is DEBUG
        
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_datetime_utc = datetime.utcfromtimestamp(exp_timestamp)
            logger.debug(f"DEBUG: Token payload 'exp' timestamp: {exp_timestamp} (UTC: {exp_datetime_utc.isoformat()})") # This logging level is DEBUG
            if exp_datetime_utc < datetime.utcnow():
                logger.warning(f"DEBUG: Token is expired. Current UTC: {datetime.utcnow().isoformat()}. Token expired UTC: {exp_datetime_utc.isoformat()}") # This logging level is DEBUG
                raise credentials_exception

        username: str = payload.get("sub")
        logger.debug(f"DEBUG: Extracted username (sub): {username}") # This logging level is DEBUG

        if username is None:
            logger.warning("DEBUG: 'sub' (username) not found in JWT payload.") # This logging level is DEBUG
            raise credentials_exception
    except JWTError as e:
        logger.error(f"DEBUG: JWT decoding error: {e}", exc_info=True) # This logging level is DEBUG
        raise credentials_exception
    except Exception as e:
        logger.error(f"DEBUG: An unexpected error occurred during token processing: {e}", exc_info=True) # This logging level is DEBUG
        raise credentials_exception

    logger.debug(f"DEBUG: Looking up user by username: {username}") # This logging level is DEBUG
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.warning(f"DEBUG: User '{username}' not found in database.") # This logging level is DEBUG
        raise credentials_exception

    logger.debug(f"DEBUG: User '{user.username}' found. Checking if active.") # This logging level is DEBUG
    if not user.is_active:
        logger.warning(f"DEBUG: User '{user.username}' is inactive.") # This logging level is DEBUG
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please contact support.",
        )

    logger.debug(f"DEBUG: User '{user.username}' is active and authenticated.") # This logging level is DEBUG
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    logger.debug(f"DEBUG: get_current_active_user entered for user: {current_user.username}") # This logging level is DEBUG
    return current_user

async def get_current_active_admin_user(current_user: User = Depends(get_current_user)):
    logger.debug(f"DEBUG: get_current_active_admin_user entered for user: {current_user.username}") # This logging level is DEBUG
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_USER]:
        logger.warning(f"DEBUG: User '{current_user.username}' (Role: {current_user.role}) attempted Admin access.") # This logging level is DEBUG
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions: Admin or Superuser role required."
        )
    return current_user

async def get_current_active_superuser(current_user: User = Depends(get_current_user)):
    logger.debug(f"DEBUG: get_current_active_superuser entered for user: {current_user.username}") # This logging level is DEBUG
    if current_user.role != UserRole.SUPER_USER:
        logger.warning(f"DEBUG: User '{current_user.username}' (Role: {current_user.role}) attempted Superuser access.") # This logging level is DEBUG
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions: Superuser role required."
        )
    return current_user
