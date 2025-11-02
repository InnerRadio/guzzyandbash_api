from __future__ import annotations # Add this line to avoid circular imports
# activity_log.py

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
# Removed PG_UUID as we are now explicitly using String(36)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base # Assuming Base is defined in app/database.py

class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    # Corrected: Use String(36) to match MySQL's CHAR(36) for UUIDs
    id = Column(
        String(36), # Changed from PG_UUID to String(36)
        primary_key=True,
        default=lambda: str(uuid.uuid4()), # Ensure default generates a string UUID
        unique=True,
        nullable=False
    )
    user_id = Column(
        String(36), # Changed from PG_UUID to String(36)
        ForeignKey('users.id'),
        nullable=False
    )
    # Corrected: Added length for VARCHAR compatibility with MySQL
    activity_type = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    metadata_json = Column(Text, nullable=True) # For storing additional structured data as JSON string

    # Relationship to User model
    user = relationship("User", back_populates="activity_logs")

    def __repr__(self):
        return f"<ActivityLog(id='{self.id}', user_id='{self.user_id}', activity_type='{self.activity_type}')>"

    # Optional: Method to easily create a new log entry
    @classmethod
    def create_log_entry(cls, user_id: uuid.UUID, activity_type: str, description: str = None, metadata_json: dict = None):
        """
        Helper method to create a new ActivityLog instance.
        metadata_json should be a dictionary and will be stored as a JSON string.
        """
        from json import dumps
        return cls(
            user_id=str(user_id), # Ensure user_id is passed as a string
            activity_type=activity_type,
            description=description,
            metadata_json=dumps(metadata_json) if metadata_json else None
        )
