# app/main.py

import sys
try:
    import bcrypt
    print(f"DEBUG: sys.path at startup: {sys.path}", file=sys.stderr)
    print(f"DEBUG: Loaded bcrypt module path: {bcrypt.__file__}", file=sys.stderr)
    print(f"DEBUG: Loaded bcrypt version: {bcrypt.__version__}", file=sys.stderr)
except AttributeError:
    print("DEBUG: bcrypt module loaded, but missing __about__ attribute.", file=sys.stderr)
except ImportError:
    print("DEBUG: bcrypt module failed to import.", file=sys.stderr)
except Exception as e:
    print(f"DEBUG: An unexpected error occurred during bcrypt import: {e}", file=sys.stderr)

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
import os

from .database import Base, SessionLocal, get_db, init_db

from app.models.user import User, UserRole, UserCreate as ModelUserCreate, UserResponse as ModelUserResponse

from app.controllers import user_types
from app.controllers import admin_reports
from app.controllers import public_reports
from app.controllers import nft_operations
from app.controllers import auth # NEW: Import the authentication router

# No longer need specific imports from app.dependencies here as auth.py handles them
# from app.dependencies import get_password_hash, verify_password, create_access_token, oauth2_scheme, get_current_user

# --- App Initialization ---
app = FastAPI(
    title="Guzzy and Bash Productions API",
    description="API for Guzzy and Bash Productions, including user management, content, and NFT operations on the XRPL.",
    version="0.0.1",
)

# --- Database Initialization (Lifecycle Events) ---
@app.on_event("startup")
def on_startup():
    init_db()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response

# --- Pydantic Models for API Requests/Responses (Authentication models are now in auth.py) ---
# Removed Token, TokenData, UserInDB, UserCreate, UserResponse from here
# If you have other base models used *only* in main.py, they would remain here.
# Assuming Token and UserCreate are now solely handled by auth.py's models.


# --- User Authentication and Authorization Endpoints (MOVED to app/controllers/auth.py) ---
# The following endpoints are now managed by auth.py's router:
# @app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# async def register_user(...): ...

# @app.post("/api/auth/token", response_model=Token)
# async def login_for_access_token(...): ...

# @app.get("/api/users/me", response_model=UserResponse)
# async def read_users_me(...): ...


# --- Include your custom API routers here ---
app.include_router(user_types.router, prefix="/api/v1")
app.include_router(admin_reports.router, prefix="/api/v1", tags=["Admin Reports"]) # ADDED TAGS
app.include_router(public_reports.router, prefix="/api/v1", tags=["Public Reports"]) # ADDED TAGS
app.include_router(nft_operations.router, prefix="/api/v1/nft", tags=["NFT Operations"]) # ADDED TAGS
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication & Users"]) # This one was already tagged!
