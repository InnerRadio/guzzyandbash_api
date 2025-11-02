from __future__ import annotations # Add this line to avoid circular imports
# app/models/affiliate.py

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.dialects.mysql import CHAR # Use CHAR for UUIDs
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pydantic import BaseModel, Field

# Assuming Base is in app.database
from ..database import Base

# --- SQLAlchemy ORM Model for Affiliate Click ---
class AffiliateClick(Base):
    """
    SQLAlchemy model for storing affiliate click tracking data.
    """
    __tablename__ = "affiliate_clicks"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    # affiliate_id refers to the 'id' of the User who generated this click
    # It is a foreign key to users.id
    affiliate_id: Mapped[str] = mapped_column(
        CHAR(36),
        ForeignKey("users.id", ondelete="CASCADE"), # Cascade delete if user is removed
        index=True, # Index for efficient lookups
        nullable=False # A click must be associated with an affiliate
    )

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True) # Supports both IPv4 and IPv6
    user_agent: Mapped[Optional[str]] = mapped_column(String(512), nullable=True) # Stores browser and OS info
    referer_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True) # The URL the user came from
    click_destination_url: Mapped[str] = mapped_column(String(2048), nullable=False) # The intended destination URL of the click

    # Optional fields for more granular tracking
    campaign_id: Mapped[Optional[str]] = mapped_column(CHAR(36), nullable=True, index=True) # UUID for a specific marketing campaign
    ad_id: Mapped[Optional[str]] = mapped_column(CHAR(36), nullable=True, index=True) # UUID for a specific advertisement

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # --- ACTIVATED AND CORRECTED: Relationship to the User model ---
    # This allows you to access the affiliate user's details from a click record: click.affiliate_user.username
    # This will be back-populated by 'affiliate_clicks' in the User model
    affiliate_user: Mapped["User"] = relationship(
        "User",
        back_populates="affiliate_clicks",
        primaryjoin="User.id == AffiliateClick.affiliate_id" # Explicit primaryjoin for clarity
    )

    def __repr__(self):
        return f"<AffiliateClick(id='{self.id}', affiliate_id='{self.affiliate_id}', timestamp='{self.timestamp}')>"


# --- NEW: SQLAlchemy ORM Model for Affiliate ---
class Affiliate(Base):
    """
    SQLAlchemy model for affiliates.
    """
    __tablename__ = "affiliates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False) # Link to a user
    referral_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    commission_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.10) # Default 10%
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship to AffiliateCommission
    commissions: Mapped[List["AffiliateCommission"]] = relationship(
        "AffiliateCommission", back_populates="affiliate", cascade="all, delete-orphan"
    )

    # NEW: Relationship to User model for the affiliate profile
    user: Mapped["User"] = relationship(
        "User", back_populates="affiliate_profile",
        primaryjoin="User.id == Affiliate.user_id" # Explicit primaryjoin
    )


    def __repr__(self):
        return f"<Affiliate(id='{self.id}', user_id='{self.user_id}', referral_code='{self.referral_code}')>"

# --- NEW: SQLAlchemy ORM Model for Affiliate Commission ---
class AffiliateCommission(Base):
    """
    SQLAlchemy model for individual affiliate commission entries.
    """
    __tablename__ = "affiliate_commissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    affiliate_id: Mapped[str] = mapped_column(String(36), ForeignKey("affiliates.id"), nullable=False)
    referred_sale_id: Mapped[Optional[str]] = mapped_column(String(36), unique=True, nullable=True) # E.g., Order ID, NFT mint ID
    referred_sale_value: Mapped[float] = mapped_column(Float, nullable=False)
    commission_amount: Mapped[float] = mapped_column(Float, nullable=False)
    commission_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    paid_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationship to Affiliate
    affiliate: Mapped["Affiliate"] = relationship("Affiliate", back_populates="commissions")

    def __repr__(self):
        return f"<AffiliateCommission(id='{self.id}', affiliate_id='{self.affiliate_id}', amount='{self.commission_amount}')>"

# --- NEW: Pydantic Schemas for Affiliate ---

class AffiliateBase(BaseModel):
    """Base Pydantic schema for Affiliate."""
    user_id: str
    referral_code: str
    commission_rate: float
    is_active: bool

class AffiliateCreate(AffiliateBase):
    """Pydantic schema for creating a new Affiliate."""
    pass

class AffiliateUpdate(BaseModel):
    """Pydantic schema for updating an existing Affiliate."""
    referral_code: Optional[str] = None
    commission_rate: Optional[float] = None
    is_active: Optional[bool] = None

class AffiliateResponse(AffiliateBase):
    """Pydantic schema for returning Affiliate via API."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AffiliateCommissionBase(BaseModel):
    """Base Pydantic schema for AffiliateCommission."""
    affiliate_id: str
    referred_sale_id: Optional[str] = None
    referred_sale_value: float
    commission_amount: float
    is_paid: bool
    paid_date: Optional[datetime] = None

class AffiliateCommissionCreate(AffiliateCommissionBase):
    """Pydantic schema for creating a new AffiliateCommission."""
    pass

class AffiliateCommissionResponse(BaseModel): # Inherit from BaseModel directly, not AffiliateCommissionBase
    """Pydantic schema for returning AffiliateCommission via API."""
    id: str
    affiliate_id: str
    referred_sale_id: Optional[str] = None
    referred_sale_value: float
    commission_amount: float
    commission_date: datetime
    is_paid: bool
    paid_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# IMPORTANT: Only Pydantic models (BaseModel) need update_forward_refs()
# SQLAlchemy ORM models do NOT have this method.
AffiliateResponse.update_forward_refs()
AffiliateCommissionResponse.update_forward_refs()
