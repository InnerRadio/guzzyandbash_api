from __future__ import annotations # Add this line to avoid circular imports
# app/models/nft.py

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.mysql import CHAR

from app.database import Base
# REMOVED: direct import of Content and User to resolve circular imports

class NFT(Base):
    __tablename__ = "nfts"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    token_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    # New UUID field for external references
    uuid: Mapped[str] = mapped_column(CHAR(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    # NEW: Add metadata_url field
    metadata_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    # Foreign key to the User who owns/minted the NFT
    owner_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=False, index=True)
    # Foreign key to the content item this NFT represents
    content_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("content_items.id"), nullable=False, index=True)

    # Timestamps
    minted_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="nfts",
        lazy="joined"
    )
    # NEW: Relationship to the Content item that this NFT represents
    # This completes the reciprocal relationship with 'nfts_minted' in the Content model
    content_item: Mapped["Content"] = relationship(
        "Content",
        back_populates="nfts_minted",
        lazy="joined" # Or "selectin" for N+1 query optimization
    )