from __future__ import annotations

# app/models/user.py
# This file defines the SQLAlchemy User model for the Guzzy and Bash Productions platform.
# It includes user authentication details, profile information, role-based access control,
# affiliate program fields, and various relationships to other models.
# Pydantic schemas related to User are now defined exclusively in app/schemas/user_schemas.py
# to maintain a clear separation of concerns (database models vs. API data contracts).

# Standard library imports
import uuid  # Used for generating unique identifiers (UUIDs)
from datetime import datetime  # Used for timestamp fields (created_at, last_updated_at)
from typing import Optional, List, Dict, Any  # Added Dict, Any for social_links
import enum # Required for defining Python Enums
import json # Added for JSON serialization/deserialization for social_links

# SQLAlchemy imports for 2.0 style declarative models
from sqlalchemy import (
    Column,        # Used to define database columns
    Integer,       # Integer column type, used for permissions_level
    String,        # String (VARCHAR) column type, used for text fields
    Boolean,       # Boolean column type, used for true/false flags
    DateTime,      # DateTime column type, used for timestamps
    ForeignKey,    # Used to define foreign key relationships to other tables
    Table          # Used for defining association tables for many-to-many relationships
)
from sqlalchemy.types import Enum as SQLEnum # For mapping Python Enums to SQL ENUM type
from sqlalchemy.sql import func # For database functions like CURRENT_TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column # For ORM relationships and declarative mapping
from sqlalchemy.dialects.mysql import CHAR # Specifically for UUID fields as CHAR(36)

from app.database import Base # Base class for SQLAlchemy models
from app.core.security import get_password_hash # For hashing passwords
from app.models.user_type_option import UserTypeOption # For UserTypeOption model

# --- Enums (User-related) ---
# Defining an Enum for user roles. This helps in enforcing valid roles within the application.
class UserRole(str, enum.Enum):
    SUPERUSER = "superuser"
    SUPER_USER = "SUPER_USER" # ADDED/CONFIRMED THIS FIX FOR DATABASE MISMATCH
    ADMIN = "admin"
    REGISTERED_USER = "registered_user"
    CONSUMER = "CONSUMER"     # ADDED/CONFIRMED THIS FIX
    CREATOR = "CREATOR"       # ADDED/CONFIRMED THIS FIX
    GUEST_PLAYER = "GUEST_PLAYER" # ADDED/CONFIRMED THIS FIX
    AFFILIATE = "affiliate"
    GUEST = "guest"

# Blueprint for role-based permissions (mapping roles to specific actions/permissions)
# This is a simplified example. In a real application, permissions might be more granular
# and stored in a database or external configuration.
ROLE_PERMISSIONS: Dict[UserRole, List[str]] = {
    UserRole.SUPERUSER: ["create_user", "read_all_users", "update_user", "delete_user",
                         "view_admin_reports", "manage_system_settings", "manage_user_types",
                         "mint_nft", "view_financial_reports", "view_token_usage"],
    UserRole.SUPER_USER: ["create_user", "read_all_users", "update_user", "delete_user", # ADDED/CONFIRMED THIS FIX
                          "view_admin_reports", "manage_system_settings", "manage_user_types",
                          "mint_nft", "view_financial_reports", "view_token_usage"],
    UserRole.ADMIN: ["read_all_users", "update_user", "delete_user", "view_admin_reports"],
    UserRole.REGISTERED_USER: ["read_self", "update_self_profile", "create_content", "view_own_content", "edit_own_content", "delete_own_content"],
    UserRole.CONSUMER: ["read_self", "view_public_content"], # ADDED/CONFIRMED THIS FIX
    UserRole.CREATOR: ["create_content", "view_own_content", "edit_own_content"], # ADDED/CONFIRMED THIS FIX
    UserRole.GUEST_PLAYER: ["view_game_content"], # ADDED/CONFIRMED THIS FIX
    UserRole.AFFILIATE: ["read_self", "update_self_profile", "view_affiliate_reports", "manage_referrals"],
    UserRole.GUEST: ["view_public_content"] # Very limited access for unauthenticated users.
}

# Helper function for JSON column
def json_serializable_column(column_type):
    """Creates a custom type for JSON data that is stored as String."""
    class JsonEncodedDict(String):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def process_bind_param(self, value, dialect):
            if value is not None:
                return json.dumps(value)
            return value

        def process_result_value(self, value, dialect):
            if value is not None:
                return json.loads(value)
            return value
    return JsonEncodedDict(column_type)

# --- SQLAlchemy Models ---

class User(Base):
    """
    SQLAlchemy model for user accounts on the platform.
    Represents the 'users' table in the database.
    """
    __tablename__ = "users"

    # Core User Identification and Authentication
    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid: Mapped[str] = mapped_column(CHAR(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())) # New UUID for external reference
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False) # For account activation/deactivation
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # For email verification
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # For top-level admin

    # NEW: Add has_api_access field
    has_api_access: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Role-Based Access Control
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role_enum", native_enum=False),
        default=UserRole.REGISTERED_USER.value,
        nullable=False
    )
    # Add permissions_level to match database schema, with a default value
    permissions_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Foreign key for user type (from user_type_options table)
    user_type_id: Mapped[Optional[str]] = mapped_column(CHAR(36), ForeignKey("user_type_options.id"), nullable=True)


    # Affiliate Program Fields
    # Each user has a unique affiliate ID generated upon creation
    affiliate_id: Mapped[str] = mapped_column(CHAR(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    # Referral code used by others to sign up under this user
    referral_code: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True, index=True)
    # The ID of the user who referred this user (self-referencing foreign key)
    referred_by_id: Mapped[Optional[str]] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=True, index=True)


    # Profile Information
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    # Social media links stored as JSON (e.g., {"twitter": "url", "linkedin": "url"})
    social_links: Mapped[Optional[Dict[str, Any]]] = mapped_column(json_serializable_column(String(2048)), nullable=True)


    # Timestamps for auditing
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


    # Relationships
    # One-to-one relationship with UserTypeOption
    user_type_option: Mapped["UserTypeOption"] = relationship("UserTypeOption", lazy="joined", backref="users")

    # Self-referencing one-to-many relationship for referrals
    referred_users: Mapped[List["User"]] = relationship(
        "User",
        remote_side=[id], # 'id' is the column on the *remote* side (the user being referred)
        back_populates="referred_by", # The 'referred_by' relationship on the referred user
        lazy="joined" # Or "selectin" for N+1 query optimization
    )
    referred_by: Mapped[Optional["User"]] = relationship(
        "User",
        remote_side=[referred_by_id], # 'referred_by_id' is the column on *this* side (the referring user)
        back_populates="referred_users", # The 'referred_users' relationship on the referring user

        lazy="joined" # Or "selectin" for N+1 query optimization
    )

    # One-to-many relationship with Content (Content owned by this user)
    owned_content: Mapped[List["Content"]] = relationship(
        "Content",
        back_populates="owner",
        lazy="joined", # Or "selectin" for N+1 query optimization
        cascade="all, delete-orphan" # Content deleted if user is deleted
    )

    # One-to-many relationship with ActivityLog (Logs related to this user)
    activity_logs: Mapped[List["ActivityLog"]] = relationship(
        "ActivityLog",
        back_populates="user",
        lazy="joined", # Or "selectin" for N+1 query optimization
        cascade="all, delete-orphan" # Activity logs deleted if user is deleted
    )

    # NEW: One-to-many relationship with NFT (NFTs minted by this user)
    # This completes the reciprocal relationship with the 'owner' in NFT.
    nfts: Mapped[List["NFT"]] = relationship( # RENAMED from minted_memorial_entries
        "NFT", # UPDATED to refer to the NFT class directly
        back_populates="owner", # This will now match the 'owner' relationship in NFT model
        lazy="joined", # Or "selectin" for N+1 query optimization
        cascade="all, delete-orphan" # Minted entries deleted if user is deleted
    )

    # Representation for debugging and utility methods
    def __repr__(self):
        # String representation for debugging, showing key user details.
        return f"<User(username='{self.username}', email='{self.email}', role='{self.role.value}')>"

    def has_permission(self, permission: str) -> bool:
        """
        Checks if the user's assigned role has a specific permission.
        This method queries the ROLE_PERMISSIONS blueprint.
        """
        return permission in ROLE_PERMISSIONS.get(self.role, [])

# NOTE: All Pydantic schemas (e.g., UserCreate, UserResponse, Token, TokenData)
# are now defined in app/schemas/user_schemas.py to keep models clean.
# keeps database model definitions clean and distinct from API data contracts.