from __future__ import annotations # Add this line to avoid circular imports
# app/models/content.py

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List # Added List for the new relationship
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, DECIMAL
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum
from sqlalchemy.dialects.mysql import CHAR # Added for CHAR type

from app.database import Base

class ContentType(str, Enum):
    ART = "Art"
    MUSIC = "Music"
    WRITING = "Writing"
    PHOTOGRAPHY = "Photography"
    VIDEO = "Video"
    OTHER = "Other"

class ContentStatus(str, Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    PENDING = "pending"
    REJECTED = "rejected"

class Content(Base):
    __tablename__ = "content_items"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid: Mapped[str] = mapped_column(CHAR(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)

    content_type: Mapped[ContentType] = mapped_column(
        SQLEnum(*[e.value for e in ContentType], name="content_type_enum", native_enum=False),
        nullable=False
    )

    content_status: Mapped[ContentStatus] = mapped_column(
        SQLEnum(*[e.value for e in ContentStatus], name="content_status_enum", native_enum=False),
        default=ContentStatus.DRAFT.value,
        nullable=False
    )

    owner_user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=False, index=True)

    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sales: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.00, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["User"] = relationship(
        "User",
        # CORRECTED: Changed back_populates to match the relationship name in the User model
        back_populates="owned_content"
    )

    # NEW: Relationship to NFTs minted from this content
    nfts_minted: Mapped[List["NFT"]] = relationship("NFT", back_populates="content_item")

    def __repr__(self):
        return f"<Content(title='{self.title}', type='{self.content_type.value}', status='{self.content_status.value}')>"