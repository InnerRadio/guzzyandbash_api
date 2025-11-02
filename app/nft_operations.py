# app/controllers/nft_operations.py
# This file defines the API endpoints related to NFT operations,
# including minting and retrieval, with integrated XRPL interaction.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

import logging

logger = logging.getLogger(__name__)

# Internal Imports
from app.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.nft import MintedMemorialEntry # SQLAlchemy model
from app.database import get_db
from app.services import nft_service # Import the NFT service
from app.schemas.user_schemas import NFTResponse # Pydantic schema for response

# NEW IMPORTS FOR XRPL INTERACTION
from xrpl.models import NFTokenMint, IssuedCurrencyAmount
from xrpl.transaction import sign
from xrpl.utils import xrp_to_drops
from app.xrpl.wallet import get_testnet_wallet, submit_transaction # Import our XRPL wallet functions
from app.config import settings # Import settings to get XRPL_WALLET_SEED

# --- NFT Metadata Models ---
class NFTAttribute(BaseModel):
    trait_type: str = Field(..., description="The type of trait (e.g., 'Category', 'Purpose')")
    value: str = Field(..., description="The value of the trait (e.g., 'Human', 'Eternal_Vow')")

class MemorialEntryMetadata(BaseModel):
    id: str = Field(..., description="Unique ID for the memorial entry (e.g., UUID from your internal system). This will be used for duplicate checking.")
    name: str = Field(..., description="Name of the memorial entry.")
    description: str = Field(..., description="Detailed description of the memorial entry.")
    image_url: Optional[str] = Field(None, description="URL to an image associated with the memorial entry.")
    attributes: List[NFTAttribute] = Field(default_factory=list, description="List of attributes for the memorial entry NFT.")

class MintMemorialEntryRequest(BaseModel):
    # Removed wallet_seed from here as it will be taken from environment variable for G&B's wallet
    token_uri: str = Field(..., description="The URI for the NFT metadata (e.g., IPFS URI).")
    memorial_entry_id: str = Field(..., description="Unique ID of the memorial entry from your system. Used for duplicate checking and MemoData.")
    category: str = Field(..., description="Category for the memorial entry, used in MemoData and NFT attributes (e.g., 'Human', 'Pet', 'Event').")
    title: str = Field(..., description="Title of the content item.")
    description: str = Field(..., description="Brief description of the content.")
    content_type: str = Field(..., description="Type of content (e.g., 'memorial_entry', 'vow', 'artwork').")
    ipfs_hash: Optional[str] = Field(None, description="IPFS hash of the content's primary data.")
    is_active: bool = Field(True, description="Indicates if the content is active and visible.")
    creator_user_id: str = Field(..., description="The ID of the user who created this content (UUID).")
    image_url: Optional[str] = Field(None, description="URL for the NFT image, if applicable.")

router = APIRouter(
    prefix="/api/v1/nft", # Add prefix for NFT operations
    tags=["NFT Operations"] # Tag for Swagger UI
)

# --- Endpoint to mint a memorial entry NFT ---
@router.post("/mint-memorial-entry-nft", response_model=NFTResponse, status_code=status.HTTP_201_CREATED)
async def mint_memorial_entry_nft(
    request_data: MintMemorialEntryRequest, # Renamed to request_data to avoid conflict with 'request' object
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> NFTResponse:
    """
    Mints a new memorial entry NFT on the XRPL Testnet using G&B Productions' wallet.
    Requires authentication.
    """
    logger.info(f"Received request to mint NFT for memorial_entry_id: {request_data.memorial_entry_id} by user: {current_user.username}")

    # Role check - remains in controller as it's an API-level authorization rule
    if current_user.role not in [UserRole.ADMIN, UserRole.CREATOR, UserRole.SUPER_USER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin, creator, or super user roles can mint NFTs."
        )

    try:
        # 1. Check for duplicate memorial_entry_id in our database FIRST
        existing_nft = nft_service.get_nft_by_memorial_entry_id(db, request_data.memorial_entry_id)
        if existing_nft:
            logger.warning(f"Duplicate mint request for memorial_entry_id: {request_data.memorial_entry_id}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An NFT for memorial entry ID '{request_data.memorial_entry_id}' has already been minted. "
                       f"Transaction Hash: {existing_nft.transaction_hash}, NFTokenID: {existing_nft.nft_token_id}",
            )

        # 2. Get the G&B Productions wallet for minting (using testnet seed from settings)
        # In a production environment, this would involve a secure signing service.
        minter_wallet = get_testnet_wallet(settings.XRPL_WALLET_SEED)
        logger.debug(f"Minter wallet address: {minter_wallet.classic_address}")

        # 3. Prepare the NFTokenMint transaction
        # The URI must be a hex string of the IPFS hash or other metadata URI
        # Ensure token_uri is valid (e.g., starts with 'ipfs://' or 'https://')
        if not request_data.token_uri.startswith(('ipfs://', 'https://')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token_uri format. Must start with 'ipfs://' or 'https://'."
            )
        
        # Construct the NFTokenMint transaction
        nft_mint_tx = NFTokenMint(
            account=minter_wallet.classic_address,
            uri=request_data.token_uri, # The URI for the NFT metadata (e.g., IPFS URI)
            # Flags can be added here if needed, e.g., tfBurnable, tfOnlyXRP, tfTransferable
            # We'll keep it simple for now.
        )
        logger.debug(f"Prepared NFTokenMint transaction: {nft_mint_tx.to_json()}")

        # 4. Sign the transaction
        # The sign method takes the transaction and the wallet object.
        signed_tx = sign(nft_mint_tx, minter_wallet)
        logger.debug(f"Signed transaction blob: {signed_tx.tx_blob}")

        # 5. Submit the signed transaction to the XRPL
        # Note: submit_transaction is a synchronous call from xrpl.py, so no await needed here
        xrpl_response_data = submit_transaction(signed_tx.tx_blob)
        logger.info(f"XRPL transaction submission response: {xrpl_response_data}")

        # Extract NFTokenID from the XRPL response (it's in the metadata)
        # This requires parsing the 'full_response' from submit_transaction
        nft_token_id = None
        if 'full_response' in xrpl_response_data and \
           'meta' in xrpl_response_data['full_response'] and \
           'AffectedNodes' in xrpl_response_data['full_response']['meta']:
            for node in xrpl_response_data['full_response']['meta']['AffectedNodes']:
                if 'CreatedNode' in node and \
                   'LedgerEntryType' in node['CreatedNode'] and \
                   node['CreatedNode']['LedgerEntryType'] == 'NFTokenPage':
                    # NFTokenID is usually found in the 'NFTokenID' field of the minted NFT
                    # within the 'NewFields' of the CreatedNode.
                    # This path might vary slightly based on XRPL response structure,
                    # but this is a common place for it.
                    if 'NewFields' in node['CreatedNode'] and \
                       'NFTokens' in node['CreatedNode']['NewFields']:
                        for nft_entry in node['CreatedNode']['NewFields']['NFTokens']:
                            if 'NFToken' in nft_entry and 'NFTokenID' in nft_entry['NFToken']:
                                nft_token_id = nft_entry['NFToken']['NFTokenID']
                                logger.info(f"Extracted NFTokenID: {nft_token_id}")
                                break
                if nft_token_id:
                    break
        
        if not nft_token_id:
            logger.warning("NFTokenID could not be extracted from XRPL response. Proceeding with 'unknown'.")
            # If NFTokenID can't be extracted, we might still proceed if transaction was tesSUCCESS
            # but it's a critical piece of data. Raise an error if it's essential.
            # For now, we'll allow it to be 'unknown' and log a warning.
            # raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to extract NFTokenID from XRPL response.")
            pass # Allow to proceed with unknown if tesSUCCESS

        # 6. Save the minted NFT details to our database
        # The nft_service.create_minted_memorial_entry is a synchronous database operation
        mint_result_db_entry = nft_service.create_minted_memorial_entry(
            db=db,
            memorial_entry_id=request_data.memorial_entry_id,
            nft_token_id=nft_token_id if nft_token_id else "unknown", # Use extracted ID or "unknown"
            transaction_hash=xrpl_response_data['transaction_hash'],
            metadata_uri=request_data.token_uri,
            minter_user_id=str(current_user.id),
            minter_username=current_user.username,
            name=request_data.title,
            description=request_data.description,
            image_uri=request_data.image_url,
            xrpl_response=str(xrpl_response_data['full_response']) # Store full XRPL response as string
        )

        # Return the success response, mapping to NFTResponse
        return NFTResponse(
            id=mint_result_db_entry.id, # Use the ID generated by our database
            memorial_entry_id=mint_result_db_entry.memorial_entry_id,
            nft_token_id=mint_result_db_entry.nft_token_id,
            transaction_hash=mint_result_db_entry.transaction_hash,
            metadata_uri=mint_result_db_entry.metadata_uri,
            minter_user_id=mint_result_db_entry.minter_user_id,
            minted_at=mint_result_db_entry.minted_at,
            name=mint_result_db_entry.name,
            description=mint_result_db_entry.description,
            image_uri=mint_result_db_entry.image_uri,
            xrpl_response=mint_result_db_entry.xrpl_response
        )

    except HTTPException:
        raise # Re-raise HTTPExceptions raised by dependencies or service for FastAPI to handle
    except Exception as e:
        logger.error(f"An unexpected error occurred during NFT minting in controller: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during NFT minting: {e}"
        )

# --- Endpoint to get all NFTs minted by the current user ---
# Using NFTResponse as the response model, assuming it maps to MintedMemorialEntry
@router.get("/nfts/my-nfts", response_model=List[NFTResponse], status_code=status.HTTP_200_OK)
async def get_nfts_by_minter_user(
    current_user: User = Depends(get_current_user), # Requires authentication
    db: Session = Depends(get_db)
) -> List[NFTResponse]:
    try:
        nfts_data = nft_service.get_nfts_by_minter_user(
            db=db,
            minter_user_id=str(current_user.id)
        )

        if not nfts_data:
            return []

        return [
            NFTResponse(
                id=nft.id,
                memorial_entry_id=nft.memorial_entry_id,
                nft_token_id=nft.nft_token_id,
                transaction_hash=nft.transaction_hash,
                metadata_uri=nft.metadata_uri,
                minter_user_id=nft.minter_user_id,
                minted_at=nft.minted_at,
                name=nft.name,
                description=nft.description,
                image_uri=nft.image_uri,
                xrpl_response=nft.xrpl_response
            ) for nft in nfts_data
        ]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"An error occurred during NFT retrieval for user {current_user.id} in controller: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during NFT retrieval: {e}")

# --- Endpoint to get a single NFT by its NFTokenID ---
# Using NFTResponse as the response model, assuming it maps to MintedMemorialEntry
@router.get("/nfts/{nft_token_id}", response_model=NFTResponse, status_code=status.HTTP_200_OK)
async def get_nft_by_token_id(
    nft_token_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        nft_data = nft_service.get_nft_by_token_id(
            db=db,
            nft_token_id=nft_token_id
        )

        if not nft_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NFT not found.")

        if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_USER] and \
           str(current_user.id) != nft_data.minter_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this NFT.")

        return NFTResponse(
            id=nft_data.id,
            memorial_entry_id=nft_data.memorial_entry_id,
            nft_token_id=nft_data.nft_token_id,
            transaction_hash=nft_data.transaction_hash,
            metadata_uri=nft_data.metadata_uri,
            minter_user_id=nft_data.minter_user_id,
            minted_at=nft_data.minted_at,
            name=nft_data.name,
            description=nft_data.description,
            image_uri=nft_data.image_uri,
            xrpl_response=nft_data.xrpl_response
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during NFT retrieval by token ID in controller: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during NFT retrieval: {e}")
