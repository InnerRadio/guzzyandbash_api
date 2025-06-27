# app/models/affiliate.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR # Use CHAR for UUIDs
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column # NEW: Import Mapped and mapped_column
from typing import Optional # NEW: Import Optional for nullable fields

from ..database import Base # Import Base from your database.py

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

    # Relationship to the User model, assuming User has 'id' as PK
    # This allows you to access the affiliate user's details from a click record: click.affiliate_user.username
    affiliate_user: Mapped["User"] = relationship("User", back_populates="affiliate_clicks")

    def __repr__(self):
        return f"<AffiliateClick(id='{self.id}', affiliate_id='{self.affiliate_id}', timestamp='{self.timestamp}')>"