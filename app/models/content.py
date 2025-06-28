# app/models/content.py

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pydantic import BaseModel

# Assuming Base is in app.database
from ..database import Base

# --- Enums for Content Properties ---
class ContentType(str, Enum):
    """Enumeration for different types of content."""
    ART = "Art"
    MUSIC = "Music"
    WRITING = "Writing"
    PHOTOGRAPHY = "Photography"
    VIDEO = "Video"
    OTHER = "Other"

class ContentStatus(str, Enum):
    """Enumeration for content publication status."""
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"

# --- SQLAlchemy ORM Model for Content ---
class Content(Base):
    """
    SQLAlchemy model for content items in the database.
    """
    __tablename__ = "content_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True) # Integer ID for simplicity
    uuid: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_type: Mapped[ContentType] = mapped_column(String(50), nullable=False)
    content_status: Mapped[ContentStatus] = mapped_column(String(50), nullable=False)
    
    # Foreign Key to User model (assuming User model exists in app.models.user)
    creator_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    
    views: Mapped[int] = mapped_column(default=0)
    sales: Mapped[float] = mapped_column(default=0.0) # Simulated sales for reports
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User model (if User model is defined)
    # creator: Mapped["User"] = relationship("User", back_populates="content_items")

    def __repr__(self):
        return f"<Content(id='{self.id}', title='{self.title}', type='{self.content_type}')>"

# --- Pydantic Schemas for Content ---

class ContentBase(BaseModel):
    """Base Pydantic schema for content."""
    title: str
    description: Optional[str] = None
    content_type: ContentType
    content_status: ContentStatus
    views: int = 0
    sales: float = 0.0

class ContentCreate(ContentBase):
    """Pydantic schema for creating new content."""
    creator_id: str # The UUID of the user creating the content

class ContentUpdate(ContentBase):
    """Pydantic schema for updating existing content."""
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[ContentType] = None
    content_status: Optional[ContentStatus] = None
    views: Optional[int] = None
    sales: Optional[float] = None

class ContentResponse(ContentBase):
    """Pydantic schema for returning content via API."""
    id: int
    uuid: str # Expose the UUID
    creator_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # This replaces orm_mode = True in Pydantic v2+

# You might have other Pydantic models for specific content types (e.g., ArtDetails, MusicTrack)
# but for basic reporting, ContentResponse should suffice.
