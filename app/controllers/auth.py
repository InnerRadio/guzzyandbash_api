# app/controllers/auth.py

import uuid # Existing: Import uuid for generating unique affiliate IDs
import random # NEW: Import random for generating unique referral codes
import string # NEW: Import string for character sets in referral code generation
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, List # Ensure List is imported

# Imports from your database and models
from ..database import get_db
# NEW: Import UserTypeOption for handling user_type_ids
from ..models.user import User, UserCreate as ModelUserCreate, UserResponse as ModelUserResponse, UserTypeOption

# Imports from your dependencies for authentication logic
from ..dependencies import get_password_hash, verify_password, create_access_token, get_current_user

# Pydantic Models for API Requests/Responses related to Auth
from pydantic import BaseModel, EmailStr, Field

# Define the router for authentication endpoints with a TAG and the CORRECT PREFIX!
router = APIRouter(
    prefix="/auth", # <--- CRITICAL FIX: ADDED PREFIX HERE!
    tags=["Authentication & Users"]
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(ModelUserResponse):
    hashed_password: str

# Helper function to generate unique referral codes
def generate_unique_referral_code(db: Session, length: int = 8) -> str:
    """Generates a unique, short alphanumeric referral code."""
    characters = string.ascii_uppercase + string.digits # A-Z, 0-9
    max_attempts = 10 # Prevent infinite loops in case of extreme collisions
    for _ in range(max_attempts):
        code = ''.join(random.choices(characters, k=length))
        # Check if code already exists in the database
        if not db.query(User).filter(User.referral_code == code).first():
            return code
    # If after max_attempts, a unique code isn't found, raise an error
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to generate a unique referral code after multiple attempts. Please try again."
    )

# --- User Authentication and Authorization Endpoints ---

# User Registration
@router.post("/register", response_model=ModelUserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: ModelUserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    db_user_by_username = db.query(User).filter(User.username == user.username).first()
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    db_user_by_email = db.query(User).filter(User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    actual_referring_affiliate_id = None
    # NEW LOGIC: Prioritize lookup by referring_referral_code
    if user.referring_referral_code:
        referring_user_by_code = db.query(User).filter(User.referral_code == user.referring_referral_code).first()
        if not referring_user_by_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Referring referral code '{user.referring_referral_code}' not found."
            )
        # Use the affiliate_id of the found referring user
        actual_referring_affiliate_id = referring_user_by_code.affiliate_id
    # Existing logic: Fallback to referring_affiliate_id if referring_referral_code was not provided
    elif user.referring_affiliate_id:
        referring_user_by_affiliate_id = db.query(User).filter(User.affiliate_id == user.referring_affiliate_id).first()
        if not referring_user_by_affiliate_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referring affiliate ID not found."
            )
        actual_referring_affiliate_id = referring_user_by_affiliate_id.affiliate_id # Use the affiliate_id of the found referring user

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        bio=user.bio,
        profile_picture_url=user.profile_picture_url,
        social_links=user.social_links,
        role=user.role if user.role else User.role.default.arg,
        permissions_level=user.permissions_level, # Ensure permissions_level is passed
        referring_affiliate_id=actual_referring_affiliate_id # This will be the affiliate_id of the referrer
    )

    # Existing logic: Generate and assign affiliate_id if not provided
    if user.affiliate_id is None:
        db_user.affiliate_id = str(uuid.uuid4())
    else:
        # If affiliate_id was provided, check its uniqueness before assigning
        if db.query(User).filter(User.affiliate_id == user.affiliate_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provided affiliate ID already exists."
            )
        db_user.affiliate_id = user.affiliate_id

    # NEW LOGIC: Generate and assign referral_code if not provided, or validate if provided
    if user.referral_code is None:
        db_user.referral_code = generate_unique_referral_code(db) # Auto-generate
    else:
        # If referral_code was provided in the payload (e.g., for vanity/pre-defined codes)
        # We need to validate its uniqueness
        if db.query(User).filter(User.referral_code == user.referral_code).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provided referral code already exists."
            )
        db_user.referral_code = user.referral_code

    # NEW LOGIC: Handle user_type_ids association
    if user.user_type_ids:
        # Fetch the UserTypeOption objects based on provided IDs
        user_types = db.query(UserTypeOption).filter(UserTypeOption.id.in_(user.user_type_ids)).all()
        # Check if all provided IDs mapped to actual UserTypeOption objects
        if len(user_types) != len(user.user_type_ids):
            # This means some provided user_type_ids were invalid
            invalid_ids = set(user.user_type_ids) - set(ut.id for ut in user_types)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"One or more user_type_ids provided are invalid: {', '.join(invalid_ids)}"
            )
        db_user.user_types = user_types # Assign the list of UserTypeOption objects

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User Login (Get Access Token)
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # CRITICAL FIX: Change 'sub' claim from user.id to user.username
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get Current User - Path adjusted to match documentation
@router.get("/users/me", response_model=ModelUserResponse) # Path here remains /users/me, combines with /auth prefix to be /auth/users/me
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Get User by ID - Path adjusted to match documentation
@router.get("/users/{user_id}", response_model=ModelUserResponse) # Path here remains /users/{user_id}, combines with /auth prefix to be /auth/users/{user_id}
async def read_user_by_id(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
