# app/controllers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

# Imports from your database and models
from ..database import get_db
from ..models.user import User, UserCreate as ModelUserCreate, UserResponse as ModelUserResponse

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

    # Validate referring_affiliate_id if provided
    if user.referring_affiliate_id:
        referring_user = db.query(User).filter(User.affiliate_id == user.referring_affiliate_id).first()
        if not referring_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referring affiliate ID not found."
            )
        actual_referring_id = referring_user.id
    else:
        actual_referring_id = None

    hashed_password = get_password_hash(user.password)

    # Create new user instance
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        bio=user.bio,
        profile_picture_url=user.profile_picture_url,
        social_links=user.social_links,
        role=user.role if user.role else User.role.default.arg,
        is_active=True,
        referring_affiliate_id=actual_referring_id
    )

    # Add to database, commit, and refresh
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
