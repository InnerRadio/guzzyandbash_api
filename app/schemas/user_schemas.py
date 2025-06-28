# app/schemas/user_schemas.py

# This file holds Pydantic schemas related to the User model,
# especially those that might cause circular import issues when
# referenced by other models' Pydantic schemas.

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field # NEW: Import Field
from enum import Enum

# Define UserRole directly in this schemas file
class UserRole(str, Enum):
    GUEST_PLAYER = "Guest/Player"
    REGISTERED_USER = "Registered User"
    CONSUMER = "Consumer"
    AFFILIATE = "Affiliate"
    CREATOR = "Creator"
    ADMIN = "Admin"
    SUPER_USER = "Super User" # Bash's high-level access

# Schema for returning UserTypeOption (Pydantic)
class UserTypeOptionResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True

# NEW: Schema for creating a new UserTypeOption
class UserTypeOptionCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = True # Default to active

    class Config:
        from_attributes = True

# NEW: Schema for updating an existing UserTypeOption
class UserTypeOptionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Pydantic schema for returning user data (excludes password hash)."""
    id: str
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    last_updated_at: datetime # Preserve last_updated_at
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    social_links: Optional[str] = None
    role: UserRole # Direct type reference is fine here, as UserRole is now in THIS file
    permissions_level: str
    affiliate_id: Optional[str] = None
    # Use direct type for UserTypeOptionResponse now that it's defined in this file
    user_types: List[UserTypeOptionResponse] = [] # Return full UserTypeOptionResponse objects
    referring_affiliate_id: Optional[str] = None
    referral_code: Optional[str] = None # NEW: Include referral_code in response

    class Config:
        from_attributes = True
        use_enum_values = True # Ensures enum values are returned as strings in JSON

# UserInDB inherits from UserResponse
class UserInDB(UserResponse):
    hashed_password: str

# IMPORTANT: Pydantic forward references. Call this after all Pydantic schemas are defined.
UserResponse.update_forward_refs()
UserTypeOptionResponse.update_forward_refs() # Ensure this is called if it references other schemas in this file
