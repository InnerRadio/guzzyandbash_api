# app/services/nft_service.py
# This file contains the business logic for NFT-related operations,
# primarily interacting with database models. XRPL interaction is handled
# by the controller and app.xrpl.wallet.

# Standard library imports
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

# SQLAlchemy imports for database session management
from sqlalchemy.orm import Session
from sqlalchemy import select # Import select for modern SQLAlchemy queries
from sqlalchemy import exc # For database exceptions

# Application-specific imports
# CORRECTED: Import NFT instead of MintedMemorialEntry
from app.models.nft import NFT
from app.models.user import User, UserRole # User and UserRole might be needed for context, but not direct CRUD here

# --- NFT Service Functions (Database Operations) ---

# CORRECTED: Function name and return type to reflect NFT model
def get_all_nfts(db: Session) -> List[NFT]:
    """
    Retrieves all NFTs from the database.
    """
    logger.info("NFT Service: Retrieving all NFTs from database.")
    # CORRECTED: Use NFT model
    return db.scalars(select(NFT)).all()

# CORRECTED: Function name and parameter/return type
def get_nft_by_id(db: Session, nft_id: str) -> Optional[NFT]:
    """
    Retrieves a specific NFT by its internal database ID.
    """
    logger.info(f"NFT Service: Retrieving NFT with internal ID '{nft_id}'.")
    # CORRECTED: Use NFT model
    return db.scalar(select(NFT).filter(NFT.id == nft_id))

# CORRECTED: Function name and parameter/return type
def get_nft_by_uuid(db: Session, nft_uuid: str) -> Optional[NFT]:
    """
    Retrieves a specific NFT by its external UUID.
    """
    logger.info(f"NFT Service: Retrieving NFT with external UUID '{nft_uuid}'.")
    # CORRECTED: Use NFT model
    return db.scalar(select(NFT).filter(NFT.uuid == nft_uuid))

# CORRECTED: Function name and parameter/return type
def get_nft_by_token_id(db: Session, token_id: int) -> Optional[NFT]:
    """
    Retrieves a specific NFT by its token ID.
    """
    logger.info(f"NFT Service: Retrieving NFT with token ID '{token_id}'.")
    # CORRECTED: Use NFT model
    return db.scalar(select(NFT).filter(NFT.token_id == token_id))

# CORRECTED: Function name and parameter/return type, and internal creation
def create_nft_record(
    db: Session,
    token_id: int,
    name: str,
    description: Optional[str],
    image_url: str,
    metadata_url: Optional[str],
    owner_id: str,
    content_id: str
) -> NFT:
    """
    Creates a new NFT record in the database.
    """
    logger.info(f"NFT Service: Creating new NFT record for token_id: {token_id}, owner_id: {owner_id}, content_id: {content_id}.")

    # The NFT model's `id` and `uuid` fields have defaults (uuid.uuid4)
    # The `minted_at` and `last_updated_at` also have defaults (func.now())
    # So, we only need to pass the explicitly required fields.
    new_nft = NFT(
        token_id=token_id,
        name=name,
        description=description,
        image_url=image_url,
        metadata_url=metadata_url,
        owner_id=owner_id,
        content_id=content_id
    )

    db.add(new_nft)
    try:
        db.commit()
        db.refresh(new_nft) # Refresh to get the generated ID and timestamps
        logger.info(f"NFT Service: Successfully saved NFT record for token_id: {token_id}. DB ID: {new_nft.id}")
        return new_nft
    except exc.IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError saving NFT record for token_id {token_id}: {e}", exc_info=True)
        raise # Re-raise for controller to handle
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error saving NFT record for token_id {token_id}: {e}", exc_info=True)
        raise # Re-raise for controller to handle

# CORRECTED: Function name and return type
def get_nfts_by_minter_user(
    db: Session,
    minter_user_id: str # Renamed parameter for consistency with NFT model's 'owner_id' if needed
) -> List[NFT]:
    """
    Retrieves all NFTs minted by a specific user from the database.
    Note: The NFT model uses 'owner_id' for the minter.
    """
    logger.info(f"NFT Service: Retrieving NFTs for owner_id: {minter_user_id} from database.")
    # CORRECTED: Use NFT model and 'owner_id' column
    return db.scalars(select(NFT).filter(NFT.owner_id == minter_user_id)).all()

# Placeholder for potential update and delete functions if needed later
# def update_nft_record(...):
#     pass

# def delete_nft_record(...):
#     pass