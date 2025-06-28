# app/models/user.py

from __future__ import annotations # NEW: Added to resolve circular import issues with type hints

import uuid
import random
import string
from datetime import datetime
from typing import Optional, List

# SQLAlchemy imports for 2.0 style
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.types import Enum as SQLEnum # Use SQLEnum for SQLAlchemy Enum type
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.mysql import CHAR # <-- NEW: Import CHAR for UUIDs

from app.database import Base # Ensure this path is correct for your setup

# NEW: Import necessary Pydantic schemas and UserRole from the new schemas file
from app.schemas.user_schemas import UserResponse, UserInDB, UserRole
from pydantic import BaseModel, EmailStr, Field # Re-import BaseModel, EmailStr, Field for other Pydantic schemas in this file


# NEW: Import the AffiliateClick model (for Affiliate System) and Affiliate model
from .affiliate import AffiliateClick, Affiliate
# NEW: UNCOMMENTED MintedMemorialEntry import
from .nft import MintedMemorialEntry


# --- User Roles and Permissions Blueprint ---
# Define permissions associated with each role. This is a blueprint for logic.
ROLE_PERMISSIONS = {
    UserRole.GUEST_PLAYER: [],
    UserRole.REGISTERED_USER: ["read_self_profile"],
    UserRole.CONSUMER: ["read_self_profile", "create_memorial_entry", "view_own_nfts"],
    UserRole.AFFILIATE: ["read_self_profile", "view_affiliate_data", "create_referral_links"],
    UserRole.CREATOR: ["read_self_profile", "manage_memorial_entries", "mint_nfts"],
    UserRole.ADMIN: ["read_self_profile", "manage_users", "view_all_reports"],
    UserRole.SUPER_USER: ["full_system_access"]
}

# Association table for User and UserTypeOption
# MOVED: This definition is now BEFORE UserTypeOption class
user_user_types = Table(
    "user_user_types",
    Base.metadata,
    Column("user_id", CHAR(36), ForeignKey("users.id"), primary_key=True),
    Column("user_type_option_id", CHAR(36), ForeignKey("user_type_options.id"), primary_key=True),
)

class UserTypeOption(Base):
    __tablename__ = "user_type_options"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Many-to-many relationship with User
    users: Mapped[List["User"]] = relationship(
        "User", secondary=user_user_types, back_populates="user_types"
    )

    def __repr__(self):
        return f"<UserTypeOption(name='{self.name}', is_active={self.is_active})>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    social_links: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True) # Stored as JSON string or similar
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.REGISTERED_USER, nullable=False)
    permissions_level: Mapped[str] = mapped_column(String(50), default="standard", nullable=False) # e.g., "standard", "elevated"
    affiliate_id: Mapped[Optional[str]] = mapped_column(CHAR(36), unique=True, index=True, nullable=True) # Unique ID for users who are affiliates
    referring_affiliate_id: Mapped[Optional[str]] = mapped_column(CHAR(36), ForeignKey("users.affiliate_id"), nullable=True) # The affiliate_id of the user who referred this user
    referral_code: Mapped[Optional[str]] = mapped_column(String(32), unique=True, index=True, nullable=True) # NEW: Short, human-readable referral code

    # Relationships
    user_types: Mapped[List["UserTypeOption"]] = relationship(
        "UserTypeOption", secondary=user_user_types, back_populates="users"
    )
    # New: Relationship for NFTs minted by this user (now uses string literal for forward reference)
    minted_nfts: Mapped[List["MintedMemorialEntry"]] = relationship(
        "MintedMemorialEntry", back_populates="minter_user"
    )
    # New: Relationship for affiliate clicks generated by this user
    affiliate_clicks: Mapped[List["AffiliateClick"]] = relationship(
        "AffiliateClick",
        back_populates="affiliate_user",
        primaryjoin="User.id == AffiliateClick.affiliate_id" # Explicit join condition
    )
    # NEW: Relationship for Affiliate profile (one-to-one)
    # This is the 'affiliate_profile' property that Affiliate model expects
    affiliate_profile: Mapped[Optional["Affiliate"]] = relationship(
        "Affiliate", back_populates="user", uselist=False, # uselist=False for one-to-one
        primaryjoin="User.id == Affiliate.user_id" # Explicit primaryjoin
    )

    # Self-referencing relationship for referrals
    referred_users: Mapped[List["User"]] = relationship(
        "User", backref="referrer", remote_side=[affiliate_id]
    )

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', role='{self.role.value}')>"

    def has_permission(self, permission: str) -> bool:
        """Checks if the user's role has a specific permission."""
        return permission in ROLE_PERMISSIONS.get(self.role, [])

# Pydantic Schemas for API (Only UserCreate, UserUpdate, Token, TokenData remain here)
class UserCreate(BaseModel):
    username: str = Field(..., max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    social_links: Optional[str] = None # Expecting a JSON string or similar
    role: Optional[UserRole] = UserRole.REGISTERED_USER # Allow role to be set on creation, default to REGISTERED_USER
    permissions_level: Optional[str] = "standard"
    affiliate_id: Optional[str] = None # Allow providing if needed for specific cases, but will be auto-generated if None
    referring_affiliate_id: Optional[str] = None
    referral_code: Optional[str] = None # Allow providing referral_code (for future custom codes) or will be auto-generated
    referring_referral_code: Optional[str] = None # NEW: Field to receive the human-readable referral code during registration

    user_type_ids: Optional[List[str]] = [] # For assigning user types by ID

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    social_links: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    permissions_level: Optional[str] = None
    affiliate_id: Optional[str] = None
    referring_affiliate_id: Optional[str] = None
    referral_code: Optional[str] = None # NEW: Allow updating referral_code
    referring_referral_code: Optional[str] = None # NEW: Allow updating referring_referral_code

    user_type_ids: Optional[List[str]] = None # For updating user types by ID

    class Config:
        from_attributes = True

# UserResponse and UserInDB are now imported from app.schemas.user_schemas

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Schema for creating a new UserTypeOption (Pydantic)
# This schema is used by UserTypeOption model's `users` relationship `back_populates`
# It's here because it's tightly coupled to the UserTypeOption model.
# If UserResponse needs it, it should import from app.schemas.user_schemas
class UserTypeOptionResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True

# IMPORTANT: Pydantic forward references. Call this after all Pydantic schemas are defined.
UserTypeOptionResponse.update_forward_refs()
