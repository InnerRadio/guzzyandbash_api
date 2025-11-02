# app/schemas/user_schemas.py
# This file defines Pydantic schemas for user-related data,
# including authentication, user profiles, and NFT responses.

from pydantic import BaseModel, EmailStr, Field, model_validator, HttpUrl, computed_field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID # Import UUID for type hinting
import enum # Import enum for UserRole

# Assuming UserRole is defined elsewhere, e.g., in app.models.user
# For schema validation, we'll define a simple Enum here if it's not directly imported
# If you have an existing UserRole enum in app.models.user, ensure it's compatible
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SUPERUSER = "superuser"
    REGISTERED_USER = "registered_user" # Changed from USER to REGISTERED_USER
    AFFILIATE = "affiliate"
    GUEST = "guest"
    # Add other roles as needed

# --- Core Authentication Schemas ---

class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None # Added for refresh token functionality

class TokenData(BaseModel):
    """Schema for data contained within a JWT token."""
    username: Optional[str] = None
    user_id: Optional[UUID] = None # Changed to UUID for strong typing
    roles: Optional[List[str]] = None # Changed to roles (list) for multiple roles

class LoginRequest(BaseModel):
    """Schema for user login requests."""
    username: str
    password: str

class ResetPasswordRequest(BaseModel): # RENAMED FROM PasswordResetRequest
    """Schema for requesting a password reset (e.g., via email)."""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Schema for confirming a password reset with a new password."""
    token: str # The reset token received by email
    new_password: str = Field(min_length=8, max_length=64, description="New password for the user.")

class PasswordChangeRequest(BaseModel):
    """Schema for a logged-in user to change their password."""
    current_password: str
    new_password: str = Field(min_length=8, max_length=64, description="New password for the user.")

# --- User Profile Schemas ---

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$", examples=["john_doe"])
    email: EmailStr = Field(examples=["john.doe@example.com"])
    password: str = Field(min_length=8, max_length=64, examples=["SecureP@ssw0rd!"])
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, examples=["John Doe"]) # Keep this for input parsing
    profile_picture_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, Any]] = None # Allow dict for social links
    role: UserRole = UserRole.REGISTERED_USER # Default role for new users.

class UserUpdate(BaseModel):
    """Schema for updating an existing user's profile."""
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=64) # Password can be updated separately
    full_name: Optional[str] = Field(None, min_length=1, max_length=100) # Keep for input parsing
    bio: Optional[str] = Field(None, max_length=1024)
    profile_picture_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, Any]] = None # Allow dict for social links
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None
    role: Optional[UserRole] = None
    has_api_access: Optional[bool] = None # Allow updating API access

class UserInDB(BaseModel):
    """Schema for user data as stored in the database (Pydantic model for internal use)."""
    id: UUID
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    role: UserRole
    permissions_level: int # Add this field as it's in the model
    user_type_id: Optional[UUID] = None # UUID for foreign key
    affiliate_id: UUID # Should be UUID
    referral_code: Optional[str] = None
    referred_by_id: Optional[UUID] = None # UUID for foreign key
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, Any]] = None
    created_at: datetime
    last_updated_at: datetime
    last_login_at: Optional[datetime] = None
    has_api_access: bool # Add this field as it's in the model

    class Config:
        from_attributes = True # Enable ORM mode

class UserResponse(BaseModel):
    """Schema for returning user data in API responses."""
    id: UUID
    email: EmailStr
    username: str
    first_name: Optional[str] = None  # Explicitly include first_name
    last_name: Optional[str] = None   # Explicitly include last_name
    # full_name will be a computed property
    role: UserRole
    is_active: bool
    is_verified: bool
    profile_picture_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, Any]] = None
    has_api_access: bool
    referral_code: Optional[str] = None
    referred_by_user_id: Optional[UUID] = None # Change to UUID
    referred_by_referral_code: Optional[str] = None
    created_at: datetime
    last_updated_at: datetime

    @computed_field
    @property
    def full_name(self) -> Optional[str]:
        """Dynamically computes full_name from first_name and last_name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return None

    class Config:
        from_attributes = True

class UserFullProfile(UserResponse):
    """
    Schema for returning a full user profile, including additional details
    not typically exposed in a standard UserResponse.
    """
    # Inherits all fields from UserResponse
    
    # Add fields from UserInDB that are relevant for a "full" profile,
    # but might not be in the basic UserResponse.
    # Exclude sensitive ones like 'hashed_password'.
    permissions_level: int
    user_type_id: Optional[UUID] = None
    referred_by_id: Optional[UUID] = None
    last_login_at: Optional[datetime] = None
    bio: Optional[str] = None # Already in UserUpdate, good to have here

    class Config:
        from_attributes = True

# --- NFT Schemas (related to User for responses) ---

class NFTBase(BaseModel):
    """Base schema for NFT data."""
    asset_id: str
    asset_contract_address: str
    owner_address: str
    token_id: str
    mint_date: datetime
    token_uri: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None # Use Dict for flexible metadata
    is_soulbound: bool = False # New field

class NFTCreate(NFTBase):
    """Schema for creating an NFT entry (e.g., after minting)."""
    # owner_id is needed when associating NFT with a user in the database
    owner_id: UUID

class NFTResponse(NFTBase):
    """Schema for returning NFT data in API responses."""
    id: UUID # Primary key for the NFT in your database
    # owner: UserResponse # Nested user response for the owner, if needed
    # Ensure all fields from the ORM model are included if using ORM mode
    # No need for owner_id here if owner object is nested.
    # If not nesting, owner_id might be useful for client to fetch owner separately.
    class Config:
        from_attributes = True # Enable ORM mode

# --- Report Schemas ---

class APIUsageReport(BaseModel):
    """Schema for API usage report."""
    date: datetime # Changed to datetime
    total_requests: int
    authenticated_requests: int
    unauthenticated_requests: int

class NFTMintActivity(BaseModel):
    """Schema for NFT minting activity report."""
    date: datetime # Changed to datetime
    total_mints: int
    successful_mints: int
    failed_mints: int

class FinancialReport(BaseModel):
    """Schema for financial overview report."""
    total_revenue: float
    total_expenses: float
    net_profit: float
    period: str

class IPFSCostReport(BaseModel):
    """Schema for IPFS costs report."""
    month: str
    storage_cost_usd: float
    retrieval_cost_usd: float
    total_cost_usd: float

class EngagementReport(BaseModel):
    """Schema for user engagement report."""
    metric: str
    value: float
    unit: str

class UsersByReferralReport(BaseModel):
    """Schema for users by referral report."""
    referral_code: str
    referred_users_count: int
    total_commissions_usd: float

class AffiliateCommissionsReport(BaseModel):
    """Schema for affiliate commissions report."""
    affiliate_id: str
    total_commissions_usd: float
    paid_commissions_usd: float
    pending_commissions_usd: float

class TokenMetricsReport(BaseModel):
    """Schema for token metrics report."""
    total_tokens_minted: int
    total_tokens_burned: int
    current_supply: int
    avg_mint_cost_usd: float
    total_transaction_fees_usd: float

class SystemHealthReport(BaseModel):
    """Schema for system health and performance report."""
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    database_connections: int
    api_response_time_ms: float

# Remember to call update_forward_refs() if your schemas have forward references or deep circularity
# e.g., if UserResponse had a field of type 'NFTResponse' that also referenced 'UserResponse'
# UserResponse.update_forward_refs()
# In this specific case, if no deep circularity, Pydantic v2 handles it better.