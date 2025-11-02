from __future__ import annotations # Add this line to avoid circular imports
# app/models/referral.py

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from pydantic import BaseModel, Field

# Assuming Base is in app.database
from ..database import Base

# --- SQLAlchemy ORM Model for Referral ---
class Referral(Base):
    """
    SQLAlchemy model for tracking referrals.
    This model primarily stores the mapping between a referred user and their referrer.
    """
    __tablename__ = "referrals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # The user who was referred
    referred_user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    
    # The user who did the referring (optional, if direct referral from an existing user)
    referrer_user_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    
    # The referral code used (optional, if referred via a general code, not a specific user)
    referral_code_used: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)
    
    # Timestamp of the referral
    referred_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    
    # Any additional metadata about the referral (e.g., source, campaign)
    referral_metadata: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # RENAMED FROM 'metadata'

    # Relationships (if User model is defined and relationships are set up there too)
    # referred_user: Mapped["User"] = relationship("User", foreign_keys=[referred_user_id], back_populates="incoming_referrals")
    # referrer_user: Mapped["User"] = relationship("User", foreign_keys=[referrer_user_id], back_populates="outgoing_referrals")

    def __repr__(self):
        return f"<Referral(id='{self.id}', referred_user_id='{self.referred_user_id}', referral_code_used='{self.referral_code_used}')>"

# --- Pydantic Schemas for Referral ---

class ReferralBase(BaseModel):
    """Base Pydantic schema for Referral."""
    referred_user_id: str
    referrer_user_id: Optional[str] = None
    referral_code_used: Optional[str] = None
    referral_metadata: Optional[str] = None # RENAMED HERE TOO

class ReferralCreate(ReferralBase):
    """Pydantic schema for creating a new Referral."""
    pass

class ReferralResponse(ReferralBase):
    """Pydantic schema for returning Referral via API."""
    id: str
    referred_at: datetime

    class Config:
        from_attributes = True

# Required for Pydantic forward references if any (e.g., self-referencing models)
ReferralResponse.update_forward_refs()
