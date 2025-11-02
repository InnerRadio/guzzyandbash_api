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
logger.setLevel(logging.DEBUG) # Explicitly set this logger's level to DEBUG

# Add a StreamHandler to ensure logs go to stderr/console if not already configured
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Internal imports
from app.database import get_db
from app.models.user import User, UserRole

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
# TEMPORARY DEBUGGING: Log the actual SECRET_KEY value
logger.debug(f"SECRET_KEY loaded: '{SECRET_KEY}'")


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
    logger.debug(f"Token created. Payload exp: {expire.isoformat()}")
    return encoded_jwt

async def get_current_user(security: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    logger.debug("get_current_user entered.")

    if not security or not security.credentials:
        logger.error("No token credentials found in security object.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = security.credentials
    logger.debug(f"Full token received from security.credentials: '{token}'")

    if not token or token.strip() == "":
        logger.error("Token string is empty or whitespace.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is empty or malformed.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug("Attempting JWT decode.")
        # TEMPORARY DEBUGGING: Log the SECRET_KEY being used for decoding
        logger.debug(f"SECRET_KEY used for decoding: '{SECRET_KEY}'")
        logger.debug(f"Token received in get_current_user for decoding: '{token}'")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT decode successful. Payload: {payload}")

        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_datetime_utc = datetime.utcfromtimestamp(exp_timestamp)
            logger.debug(f"Token payload 'exp' timestamp: {exp_timestamp} (UTC: {exp_datetime_utc.isoformat()})")
            if exp_datetime_utc < datetime.utcnow():
                logger.warning(f"Token is expired. Current UTC: {datetime.utcnow().isoformat()}. Token expired UTC: {exp_datetime_utc.isoformat()}")
                raise credentials_exception

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

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    logger.debug(f"get_current_active_user entered for user: {current_user.username}")
    return current_user

async def get_current_user_id(current_user: User = Depends(get_current_user)) -> str:
    """
    Dependency that gets the current authenticated user and returns their ID as a string.
    """
    logger.debug(f"get_current_user_id entered for user: {current_user.username}")
    return str(current_user.id) # Ensure the ID is a string

async def get_current_active_admin_user(current_user: User = Depends(get_current_user)):
    logger.debug(f"get_current_active_admin_user entered for user: {current_user.username}")
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPERUSER]:
        logger.warning(f"User '{current_user.username}' (Role: {current_user.role}) attempted Admin access.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions: Admin or Superuser role required."
        )
    return current_user

async def get_current_active_superuser(current_user: User = Depends(get_current_user)):
    logger.debug(f"get_current_active_superuser entered for user: {current_user.username}")
    if current_user.role != UserRole.SUPERUSER:
        logger.warning(f"User '{current_user.username}' (Role: {current_user.role}) attempted Superuser access.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions: Superuser role required."
        )
    return current_user
