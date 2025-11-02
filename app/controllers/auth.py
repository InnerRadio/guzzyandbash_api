# app/controllers/auth.py
# This file handles authentication-related API endpoints, including user login,
# token generation, password hashing, and user creation.

# Standard library imports
from datetime import timedelta, datetime
from typing import Annotated, Optional, List, Any
import uuid
import random
import string
import enum
import logging
import sys

# FastAPI and Pydantic imports
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# Security utilities
from jose import JWTError, jwt
from passlib.context import CryptContext

# Database and model imports
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user_schemas import UserCreate, UserResponse, Token, ResetPasswordRequest, PasswordResetConfirm, LoginRequest
import app.crud.user as crud

# Import the settings object from app.core.config
from app.core.config import settings

# Import only functions from app.core.security
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)

# Configuration for logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# DEBUGGING LINE: This will print the path of this file when it's loaded
print(f"DEBUG: app.controllers.auth is loaded from: {__file__}")


# FastAPI router for authentication endpoints
router = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

# OAuth2PasswordBearer for handling token security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    logger.debug(f"Received registration request for username: {user_create.username}, email: {user_create.email}")

    # Check if user already exists by email or username
    if crud.get_user_by_email(db, email=user_create.email):
        logger.warning(f"Registration attempt with existing email: {user_create.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if crud.get_user_by_username(db, username=user_create.username):
        logger.warning(f"Registration attempt with existing username: {user_create.username}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Generate a unique affiliate_id for ALL new users, as per your requirement.
    affiliate_id = str(uuid.uuid4()) # Generate unconditionally for every new registration

    user = crud.create_user(
        db=db,
        user=user_create,
        affiliate_id=affiliate_id,
    )

    if user is None:
        logger.error(f"Failed to create user after checks for username: {user_create.username}, email: {user_create.email}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed due to an internal error or duplicate entry not caught earlier.")

    # Send welcome email as a background task
    login_url = str(request.url).replace("/register", "/login") # Construct login URL dynamically
    background_tasks.add_task(send_welcome_email, user.email, user.username, login_url)
    logger.info(f"Scheduled welcome email for new user: {user.username}")

    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    logger.debug(f"Login attempt for username: {form_data.username}")
    user = crud.get_user_by_username(db, username=form_data.username)

    # If user is not found, or password verification fails, raise an HTTPException
    # The temporary debug detail has been removed for security in a live environment.
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password", # Reverted to generic message
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # Convert UserRole enum to string for JWT claims
    user_roles = [role.value for role in user.role] if isinstance(user.role, list) else [user.role.value] if user.role else []


    access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "roles": user_roles},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": str(user.id)},
        expires_delta=refresh_token_expires
    )
    logger.info(f"User {user.username} successfully logged in and tokens generated.")
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/token/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str = Depends(oauth2_scheme), # Expect refresh token in Authorization header
    db: Session = Depends(get_db)
):
    """
    Refreshes the access token using a valid refresh token.
    """
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token payload")

        user = crud.get_user(db, user_id=user_id) # Use get_user by ID for refresh
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        # Convert UserRole enum to string for JWT claims
        user_roles = [role.value for role in user.role] if isinstance(user.role, list) else [user.role.value] if user.role else []


        # Generate a new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": user.username, "user_id": str(user.id), "roles": user_roles},
            expires_delta=access_token_expires
        )

        logger.info(f"Access token refreshed for user: {username}")
        return {"access_token": new_access_token, "token_type": "bearer", "refresh_token": refresh_token} # Return original refresh token
    except JWTError:
        logger.warning("Invalid refresh token provided.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

# TEMPORARY: The debug-reset-superuser-password endpoint has been removed for security.

@router.post("/password-reset-request", status_code=status.HTTP_200_OK)
async def request_password_reset(
    password_reset_request: ResetPasswordRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db)
):
    logger.debug(f"Password reset request for email: {password_reset_request.email}")
    user = crud.get_user_by_email(db, email=password_reset_request.email)
    if not user:
        # For security, do not reveal if the email is not registered
        logger.warning(f"Password reset requested for unregistered email: {password_reset_request.email}")
        return {"message": "If a matching account is found, a password reset email will be sent."}

    # Generate a password reset token (e.g., a short-lived JWT or a UUID)
    reset_token_data = {"sub": user.username, "user_id": str(user.id), "type": "password_reset"}
    reset_token_expires = timedelta(minutes=60) # Token valid for 60 minutes
    reset_token = create_access_token(reset_token_data, expires_delta=reset_token_expires)

    # Construct reset URL
    # Assuming your frontend handles /reset-password?token=<token>
    reset_url = f"{request.base_url}reset-password?token={reset_token}"
    logger.info(f"Generated password reset token for {user.username}. Reset URL: {reset_url}")

    # Send email in background
    background_tasks.add_task(send_reset_password_email, user.email, user.username, reset_url)
    logger.info(f"Scheduled password reset email for user: {user.username}")

    return {"message": "If a matching account is found, a password reset email will be sent."}

@router.post("/password-reset-confirm", status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    password_reset: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    logger.debug("Password reset confirmation attempt.")
    try:
        payload = jwt.decode(password_reset.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        token_type: str = payload.get("type")

        if username is None or user_id is None or token_type != "password_reset":
            logger.warning("Invalid token payload for password reset confirmation.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")

    except JWTError as e:
        logger.warning(f"Invalid or expired JWT for password reset: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update the user's password
    hashed_password = get_password_hash(password_reset.new_password)
    updated_user = crud.update_user_password(db, user=user, hashed_password=hashed_password)

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update password")

    return {"message": "Password has been successfully reset."}

# Dummy email sending function (replace with actual email service)
async def send_welcome_email(email_to: str, username: str, login_url: str):
    logger.info(f"Sending welcome email to {email_to} for user {username} with login link {login_url}")
    # In a real application, you would integrate with an email service here (e.g., SendGrid, Mailgun)
    pass

async def send_reset_password_email(email_to: str, username: str, reset_url: str):
    logger.info(f"Sending password reset email to {email_to} for user {username} with reset link {reset_url}")
    # In a real application, integrate with an email service here
    pass