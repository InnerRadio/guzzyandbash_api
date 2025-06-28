# app/controllers/nft_operations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

# Internal Imports
from app.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.nft import MintedMemorialEntry, MintedMemorialEntryResponse
from app.database import get_db
from app.services import nft_service

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
    wallet_seed: str = Field(..., description="The seed for the XRPL wallet to mint the NFT.")
    token_uri: str = Field(..., description="The URI for the NFT metadata (e.g., IPFS URI).")
    memorial_entry_id: str = Field(..., description="Unique ID of the memorial entry from your system. Used for duplicate checking and MemoData.")
    category: str = Field(..., description="Category for the memorial entry, used in MemoData and NFT attributes (e.g., 'Human', 'Pet', 'Event').")

router = APIRouter()

# --- Endpoint to mint a memorial entry NFT ---
@router.post("/mint-memorial-entry-nft", status_code=status.HTTP_200_OK)
async def mint_memorial_entry_nft(
    request: MintMemorialEntryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Role check - remains in controller as it's an API-level authorization rule
    if current_user.role not in [UserRole.ADMIN, UserRole.CREATOR, UserRole.SUPER_USER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin, creator, or super user roles can mint NFTs."
        )

    try:
        # Delegate to nft_service for minting logic
        mint_result = await nft_service.mint_memorial_entry_nft_dummy(
            db=db, # Pass db session, though dummy service won't use it directly
            memorial_entry_id=request.memorial_entry_id,
            token_uri=request.token_uri,
            category=request.category,
            minter_user_id=current_user.id, # Use current_user.id (UUID) for minter_user_id
            minter_username=current_user.username # CORRECTED: Pass the username
        )

        # Handle simulated duplicate response
        if mint_result.get("is_duplicate"):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An NFT for memorial entry ID '{request.memorial_entry_id}' has already been minted (simulated). Transaction Hash: {mint_result.get('transaction_hash')}, NFTokenID: {mint_result.get('nft_token_id')}",
            )

        # Return the success response from the service
        return mint_result

    except HTTPException:
        raise # Re-raise HTTPExceptions raised by dependencies or service for FastAPI to handle
    except Exception as e:
        logger.error(f"An unexpected error occurred during NFT minting in controller: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during NFT minting: {e}"
        )

# --- Endpoint to get all NFTs minted by the current user ---
@router.get("/nfts/my-nfts", response_model=List[MintedMemorialEntryResponse], status_code=status.HTTP_200_OK)
async def get_nfts_by_minter_user(
    current_user: User = Depends(get_current_user), # Requires authentication
    db: Session = Depends(get_db) # Pass db session, though dummy service won't use it directly
):
    try:
        # Delegate to nft_service for retrieval logic
        nfts_data = await nft_service.get_nfts_by_minter_user_dummy(
            db=db,
            minter_user_id=current_user.id # Use current_user.id (UUID)
        )

        if not nfts_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No NFTs found for this user (simulated).")

        return nfts_data # Already in the correct format from the service

    except HTTPException:
        raise # Re-raise HTTPExceptions
    except Exception as e:
        logger.error(f"An error occurred during NFT retrieval for user {current_user.id} in controller: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during NFT retrieval: {e}")

# --- Endpoint to get a single NFT by its NFTokenID ---
@router.get("/nfts/{nft_token_id}", response_model=MintedMemorialEntryResponse, status_code=status.HTTP_200_OK)
async def get_nft_by_token_id(
    nft_token_id: str,
    current_user: User = Depends(get_current_user), # Requires authentication
    db: Session = Depends(get_db) # Pass db session, though dummy service won't use it directly
):
    try:
        # Delegate to nft_service for retrieval logic
        nft_data = await nft_service.get_nft_by_token_id_dummy(
            db=db,
            nft_token_id=nft_token_id
        )

        if not nft_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NFT not found (simulated).")

        # Permissions check: Only ADMIN, SUPER_USER, or the minter_user can view details
        if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_USER] and \
           current_user.id != nft_data.minter_user_id: # Access directly from Pydantic model
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this NFT.")

        return nft_data

    except HTTPException:
        raise # Re-raise HTTPExceptions
    except Exception as e:
        logger.error(f"An unexpected error occurred during NFT retrieval by token ID in controller: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during NFT retrieval: {e}")

