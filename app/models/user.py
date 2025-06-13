# app/models/user.py
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
# Removed: from sqlalchemy.dialects.mysql import UUID (no longer needed as we use String(36))

from app.database import Base

from pydantic import BaseModel, EmailStr, Field

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
    UserRole.REGISTERED_USER: ["read_public_content", "save_reading_session"],
    UserRole.CONSUMER: ["read_public_content", "save_reading_session"],
    UserRole.AFFILIATE: ["read_public_content", "save_reading_session", "generate_affiliate_link", "view_commissions"],
    UserRole.CREATOR: ["read_public_content", "save_reading_session", "manage_content", "create_reading_session", "upload_media", "view_creator_dashboard"],
    UserRole.ADMIN: ["read_public_content", "save_reading_session", "manage_content", "create_reading_session", "upload_media", "view_creator_dashboard", "manage_users", "view_system_logs"],
    UserRole.SUPER_USER: ["read_public_content", "save_reading_session", "manage_content", "create_reading_session", "upload_media", "view_creator_dashboard", "manage_users", "view_system_logs", "full_system_access"]
}

# --- SQLAlchemy Models (Database Schemas) ---
# Association Table for User and UserTypeOption (Many-to-Many)
user_user_type_options_association_table = Table(
    'user_user_type_options_association',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('user_type_option_id', Integer, ForeignKey('user_type_options.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    social_links: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.REGISTERED_USER)
    permissions_level: Mapped[str] = mapped_column(String(255), default="standard_user")
    affiliate_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True, nullable=True)
    referring_affiliate_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)

    # Many-to-many relationship with UserTypeOption
    user_type_options: Mapped[List["UserTypeOption"]] = relationship(
        "UserTypeOption",
        secondary=user_user_type_options_association_table,
        back_populates="users"
    )

    # Relationship to the referring user (self-referencing)
    referred_by: Mapped[Optional["User"]] = relationship('User', remote_side=[id], backref='referred_users')


    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

# Schema for UserTypeOption (Database Model)
class UserTypeOption(Base):
    __tablename__ = "user_type_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Many-to-many relationship with User
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_user_type_options_association_table,
        back_populates="user_type_options" # <-- CORRECTED LINE
    )

    def __repr__(self):
        return f"<UserTypeOption(name='{self.name}')>"

# --- Pydantic Schemas (for API Request/Response validation) ---
class UserCreate(BaseModel):
    username: str = Field(..., max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    social_links: Optional[str] = None
    role: Optional[UserRole] = UserRole.REGISTERED_USER
    permissions_level: Optional[str] = "standard_user"
    affiliate_id: Optional[str] = None
    user_types: Optional[List[int]] = [] # List of user_type_option IDs
    referring_affiliate_id: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    social_links: Optional[str] = None
    role: Optional[UserRole] = None
    permissions_level: Optional[str] = None
    affiliate_id: Optional[str] = None
    user_types: Optional[List[int]] = None # List of user_type_option IDs to update
    referring_affiliate_id: Optional[str] = None # Ensure type is string for UUIDs


class UserTypeOptionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    last_updated_at: datetime
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    social_links: Optional[str] = None
    role: UserRole
    permissions_level: str
    affiliate_id: Optional[str] = None
    user_types: List["UserTypeOptionResponse"] = [] # Default to empty list if no types
    referring_affiliate_id: Optional[str] = None # Updated to String(36) for UUIDs


    class Config:
        from_attributes = True
        use_enum_values = True


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
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for a single user type option value (for assigning to a user via ID)
class UserTypeOptionAssign(BaseModel):
    user_type_option_id: int

# Schema for UserTypeOption response (Pydantic) - for display
class UserTypeOptionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True