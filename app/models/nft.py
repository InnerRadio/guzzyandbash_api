# app/models/nft.py

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR, MEDIUMTEXT
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Assuming Base is in app.database
from ..database import Base

# NEW: Import UserResponse from the new schemas file
from app.schemas.user_schemas import UserResponse # Corrected import path
from pydantic import BaseModel

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
    image_uri: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    # Store full XRPL response for debugging/auditing
    xrpl_response: Mapped[Optional[str]] = mapped_column(MEDIUMTEXT, nullable=True)

    # Define relationship to the User model (SQLAlchemy handles forward refs with from __future__ annotations)
    minter_user: Mapped["User"] = relationship("User", back_populates="minted_nfts")

    def __repr__(self):
        return f"<MintedMemorialEntry(id='{self.id}', memorial_entry_id='{self.memorial_entry_id}', nft_token_id='{self.nft_token_id}')>"


# Pydantic Schema for returning MintedMemorialEntry via API
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

    # Include nested UserResponse to show minter details.
    # Now imported directly from app.schemas.user_schemas
    minter_user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Explicitly call update_forward_refs() for this Pydantic model.
# This resolves any *remaining* string literal forward references within this specific Pydantic model.
MintedMemorialEntryResponse.update_forward_refs()
