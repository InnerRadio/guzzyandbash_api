from __future__ import annotations

# app/models/user_type_option.py

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Text # Import Text
from sqlalchemy.dialects.mysql import CHAR # Removed TINYTEXT as it's no longer directly used
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class UserTypeOption(Base):
    """
    SQLAlchemy model for managing different user type options (e.g., 'admin', 'registered_user', 'affiliate').
    These are distinct from user roles which are assigned to individual users and can be more dynamic.
    This model defines the available, configurable user types in the system.
    """
    __tablename__ = "user_type_options"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True) # e.g., "admin", "registered_user"
    # CORRECTED: Changed TINYTEXT to Text for better autogenerate compatibility
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # A brief description of the user type
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False) # Whether this user type is currently available for assignment

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<UserTypeOption(name='{self.name}', is_active={self.is_active})>"