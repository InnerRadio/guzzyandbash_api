# app/models/user.py

from __future__ import annotations # NEW: Added to resolve circular import issues with type hints

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List

# SQLAlchemy imports for 2.0 style
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.types import Enum as SQLEnum # Use SQLEnum for SQLAlchemy Enum type
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.mysql import CHAR # <-- NEW: Import CHAR for UUIDs

from app.database import Base # Ensure this path is correct for your setup

# Pydantic imports for schemas
from pydantic import BaseModel, EmailStr, Field

# REMOVED: Import the new MintedMemorialEntry model (from NFT work)
# This import is no longer necessary here as relationships use string forward references,
# and direct module-level import causes circular dependency issues with Pydantic.
# from .nft import MintedMemorialEntry # <--- REMOVED

# NEW: Import the AffiliateClick model (for Affiliate System)
from .affiliate import AffiliateClick # <--- NEW IMPORT

# --- User Roles and Permissions Blueprint ---
# Defines explicit roles for all interactions within Guzzy and Bash Productions
class UserRole(str, Enum):
    GUEST_PLAYER = "Guest/Player"
    REGISTERED_USER = "Registered User"
    CONSUMER = "Consumer"
    AFFILIATE = "Affiliate"
    CREATOR = "Creator"
    ADMIN = "Admin"
    SUPER_USER = "Super User" # Bash's high-level access

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
        "User", secondary="user_user_types", back_populates="user_types"
    )

    def __repr__(self):
        return f"<UserTypeOption(name='{self.name}', is_active={self.is_active})>"

# Association table for User and UserTypeOption
user_user_types = Table(
    "user_user_types",
    Base.metadata,
    Column("user_id", CHAR(36), ForeignKey("users.id"), primary_key=True),
    Column("user_type_option_id", CHAR(36), ForeignKey("user_type_options.id"), primary_key=True),
)

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
        "AffiliateClick", back_populates="affiliate_user"
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

# Pydantic Schemas for API
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
    affiliate_id: Optional[str] = None
    referring_affiliate_id: Optional[str] = None
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
    user_type_ids: Optional[List[str]] = None # For updating user types by ID

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
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
    role: UserRole
    permissions_level: str
    affiliate_id: Optional[str] = None
    user_types: List["UserTypeOptionResponse"] = [] # Return full UserTypeOptionResponse objects
    referring_affiliate_id: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True # Ensures enum values are returned as strings in JSON

class UserInDB(UserResponse):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Schema for creating a new UserTypeOption (Pydantic)
class UserTypeOptionCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    is_active: bool = True

# Schema for updating an existing UserTypeOption (Pydantic)
class UserTypeOptionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None

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
