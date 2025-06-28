# /var/www/tarot-api/guzzy_and_bash_productions/app/services/nft_service.py

import uuid
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import random
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

# NEW: Import the actual Pydantic models
from app.models.nft import MintedMemorialEntryResponse
from app.models.user import UserResponse, UserRole # UserRole needed for dummy UserResponse

# Dummy data for MintedMemorialEntry. We'll simulate DB storage here.
# Now stores actual MintedMemorialEntryResponse objects.
_dummy_minted_nfts: List[MintedMemorialEntryResponse] = []

# REMOVED: DummyMintedMemorialEntryResponse class is no longer needed.


async def mint_memorial_entry_nft_dummy(
    db: Session, # Session is still passed, but not used for dummy data
    memorial_entry_id: str,
    token_uri: str,
    category: str,
    minter_user_id: str, # This is the UUID
    minter_username: str # NEW: We need the username to create a dummy UserResponse
) -> Dict[str, Any]:
    """
    Placeholder: Simulates minting a memorial entry NFT.
    Checks for duplicates and generates a dummy NFTokenID and transaction hash.
    Returns a dictionary matching the controller's expected success response.
    """
    logger.info(f"NFT Service: Simulating mint for memorial_entry_id: {memorial_entry_id}, by user_id: {minter_user_id}, username: {minter_username}")

    # Simulate duplicate check from the dummy storage
    for nft in _dummy_minted_nfts:
        if nft.memorial_entry_id == memorial_entry_id:
            logger.warning(f"NFT Service: Duplicate memorial_entry_id detected: {memorial_entry_id}")
            # Simulate a 409 Conflict, but return a dict as if it was a successful lookup
            return {
                "message": "NFT for memorial entry ID already minted (dummy).",
                "transaction_hash": nft.transaction_hash,
                "nft_token_id": nft.nft_token_id,
                "initiated_by_user": minter_username, # Changed to username for consistency
                "xrpl_response_result": "dummy_duplicate_success",
                "is_duplicate": True # Custom field to indicate this is a simulated duplicate response
            }

    # Simulate XRPL transaction hash and NFTokenID
    dummy_transaction_hash = f"0x{uuid.uuid4().hex}"
    dummy_nft_token_id = f"0008{uuid.uuid4().hex[:16].upper()}" # Simulate a valid XRPL NFTokenID format

    # Create a dummy UserResponse for the minter_user field
    dummy_minter_user = UserResponse(
        id=minter_user_id,
        username=minter_username,
        email=f"{minter_username}@example.com", # Dummy email
        is_active=True,
        created_at=datetime.utcnow() - timedelta(days=random.randint(10, 100)), # Dummy date
        last_updated_at=datetime.utcnow(),
        role=UserRole.CREATOR, # Assume creator role for minters
        permissions_level="standard"
    )

    # Instantiate MintedMemorialEntryResponse directly
    new_minted_entry = MintedMemorialEntryResponse(
        id=str(uuid.uuid4()), # Generate a new UUID for the NFT record itself
        memorial_entry_id=memorial_entry_id,
        nft_token_id=dummy_nft_token_id,
        transaction_hash=dummy_transaction_hash,
        metadata_uri=token_uri,
        # xrpl_response is omitted from MintedMemorialEntryResponse, as per models/nft.py
        minter_user_id=minter_user_id,
        minted_at=datetime.utcnow(), # Use UTC now
        name=f"Memorial for {memorial_entry_id}", # Dummy name
        description=f"A digital memorial for category: {category}", # Dummy description
        image_uri=f"{token_uri}/image.jpg", # Dummy image_uri
        minter_user=dummy_minter_user # Assign the dummy UserResponse
    )

    _dummy_minted_nfts.append(new_minted_entry)
    logger.info(f"NFT Service: Successfully simulated mint for {memorial_entry_id}. NFTokenID: {dummy_nft_token_id}")

    return {
        "message": "NFT mint transaction submitted successfully to XRPL Testnet (dummy).",
        "transaction_hash": dummy_transaction_hash,
        "nft_token_id": dummy_nft_token_id,
        "initiated_by_user": minter_username, # Changed to username for consistency
        "xrpl_response_result": "tesSUCCESS"
    }


async def get_nfts_by_minter_user_dummy(
    db: Session, # Session is still passed, but not used for dummy data
    minter_user_id: str
) -> List[MintedMemorialEntryResponse]: # CORRECTED: Return type is List[MintedMemorialEntryResponse]
    """
    Placeholder: Retrieves all NFTs minted by a specific user from dummy data.
    Returns a list of MintedMemorialEntryResponse objects.
    """
    logger.info(f"NFT Service: Retrieving NFTs for minter_user_id: {minter_user_id} (dummy)")
    
    # Filter dummy NFTs by minter_user_id
    # _dummy_minted_nfts already stores MintedMemorialEntryResponse objects
    user_nfts = [nft for nft in _dummy_minted_nfts if nft.minter_user_id == minter_user_id]

    if not user_nfts:
        logger.warning(f"NFT Service: No dummy NFTs found for user: {minter_user_id}")
        return [] # Return empty list if no NFTs found

    return user_nfts


async def get_nft_by_token_id_dummy(
    db: Session, # Session is still passed, but not used for dummy data
    nft_token_id: str
) -> Optional[MintedMemorialEntryResponse]: # CORRECTED: Return type is Optional[MintedMemorialEntryResponse]
    """
    Placeholder: Retrieves a single NFT by its NFTokenID from dummy data.
    Returns a MintedMemorialEntryResponse object or None.
    """
    logger.info(f"NFT Service: Retrieving NFT by token ID: {nft_token_id} (dummy)")

    # Find the NFT in dummy storage
    for nft in _dummy_minted_nfts:
        if nft.nft_token_id == nft_token_id:
            return nft
    
    logger.warning(f"NFT Service: Dummy NFT with NFTokenID '{nft_token_id}' not found.")
    return None # Return None if not found
