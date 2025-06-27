# app/models/nft.py

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, ForeignKey, Text # Import Text for large text fields
from sqlalchemy.dialects.mysql import CHAR # NEW: Import CHAR for consistency, though it might already be imported
from sqlalchemy.orm import relationship, Mapped, mapped_column # Import Mapped and mapped_column for SQLAlchemy 2.0 style

# Assuming Base is in app.database
from ..database import Base

# NEW: Import UserResponse for nested Pydantic schema
# It's important to keep this import as MintedMemorialEntryResponse depends on it.
from app.models.user import UserResponse
from pydantic import BaseModel # NEW: Import BaseModel for Pydantic schemas

class MintedMemorialEntry(Base):
    __tablename__ = "minted_memorial_entries"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    memorial_entry_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    nft_token_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False) # XRPL NFT ID is 64 hex chars
    transaction_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False) # XRPL transaction hash
    minter_user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=False)
    minted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Optional: Store some metadata for easier lookup without querying XRPL or IPFS
    metadata_uri: Mapped[Optional[str]] = mapped_column(String(512), nullable=True) # IPFS URI
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    image_uri: Mapped[Optional[str]] = mapped_column(String(512), nullable=True) # This looks like a duplicate of metadata_uri, but kept if you have a specific use.

    # Store full XRPL response for debugging/auditing
    xrpl_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


    # Define relationship to the User model
    # The 'back_populates' argument must match the name of the relationship property in the User model ('minted_nfts')
    minter_user: Mapped["User"] = relationship("User", back_populates="minted_nfts")

    def __repr__(self):
        return f"<MintedMemorialEntry(id='{self.id}', memorial_entry_id='{self.memorial_entry_id}', nft_token_id='{self.nft_token_id}')>"


# NEW: Pydantic Schema for returning MintedMemorialEntry via API
class MintedMemorialEntryResponse(BaseModel):
    id: str
    memorial_entry_id: str
    nft_token_id: str
    transaction_hash: str
    minter_user_id: str
    minted_at: datetime
    metadata_uri: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    image_uri: Optional[str] = None
    # The full xrpl_response can be very large. We are omitting it from this general
    # response model to keep payloads light. A separate endpoint could provide the full detail.
    # xrpl_response: Optional[str] = None # Omitted by default for performance/brevity

    # Include nested UserResponse to show minter details
    # IMPORTANT: Use 'UserResponse' directly, not a string forward reference,
    # because we are importing it directly above.
    minter_user: Optional[UserResponse] = None


    class Config:
        from_attributes = True # This replaces orm_mode = True in Pydantic v2+
        # Json serialization of datetime objects is handled by FastAPI's default JSONResponse automatically

# NEW: Explicitly call update_forward_refs() after all models are defined
# This helps Pydantic resolve nested references like UserResponse within MintedMemorialEntryResponse.
# This should happen after all potentially referenced models are imported.
MintedMemorialEntryResponse.update_forward_refs()
