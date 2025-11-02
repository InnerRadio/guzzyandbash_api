# app/controllers/nft_operations.py
# This file defines the API endpoints related to NFT operations,
# including minting and retrieval, with integrated XRPL interaction.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import asyncio
import sys
import logging
import json # NEW: Import json for logging full response

# --- Custom Logger Configuration for this module ---
# Get the logger for this module
logger = logging.getLogger(__name__)
# Set the logging level to DEBUG to capture all messages
logger.setLevel(logging.DEBUG)

# Create handlers for stdout and stderr if they don't already exist
# This prevents adding multiple handlers on successive reloads in development
if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
    # Create a handler that writes log messages to sys.stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG) # Set handler level to DEBUG
    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(levelname)s: %(asctime)s - %(name)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    # Add the handler to the logger
    logger.addHandler(stdout_handler)

    # Create a handler that writes log messages to sys.stderr (for errors)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR) # Only ERROR and above to stderr
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

# Internal Imports
from app.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.nft import NFT # SQLAlchemy model
from app.database import get_db
from app.services import nft_service # Import the NFT service
from app.schemas.user_schemas import NFTResponse, UserResponse # Import UserResponse here

# NEW IMPORTS FOR XRPL INTERACTION
from xrpl.models import NFTokenMint, IssuedCurrencyAmount
from xrpl.transaction import sign
from xrpl.utils import xrp_to_drops, str_to_hex
from xrpl.asyncio.ledger import get_latest_validated_ledger_sequence as async_get_latest_validated_ledger_sequence
from xrpl.asyncio.clients import AsyncJsonRpcClient, AsyncWebsocketClient, XRPLRequestFailureException
from xrpl.asyncio.transaction import submit_and_wait

# Application configuration imports
from app.core.config import settings # Ensure settings is imported here for use in this file

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
    prefix="/nft",
    tags=["NFT Operations"]
)

# --- Endpoint to mint a memorial entry NFT ---
@router.post("/mint-memorial-entry-nft", response_model=NFTResponse, status_code=status.HTTP_201_CREATED)
async def mint_memorial_entry_nft(
    request_data: MintMemorialEntryRequest,
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
        from xrpl.wallet import Wallet
        
        # *** NEW CRITICAL CHECK ADDED HERE ***
        if not settings.XRPL_WALLET_SEED:
            logger.error("XRPL_WALLET_SEED is missing in the environment or settings. Cannot mint NFT.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error: XRPL minting wallet seed is missing."
            )

        minter_wallet = Wallet.from_seed(seed=settings.XRPL_WALLET_SEED)
        logger.info(f"Minter wallet address: {minter_wallet.classic_address}")

        # Use AsyncJsonRpcClient for ledger sequence (it's fine for this)
        async_client = AsyncJsonRpcClient(settings.XRPL_NETWORK_URL)
        
        # Get the latest validated ledger sequence
        current_ledger_sequence = await async_get_latest_validated_ledger_sequence(async_client)
        
        last_ledger_sequence = current_ledger_sequence + 20
        logger.debug(f"Current ledger sequence: {current_ledger_sequence}, Last ledger sequence for transaction: {last_ledger_sequence}")

        if not request_data.token_uri.startswith(('ipfs://', 'https://')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token_uri format. Must start with 'ipfs://' or 'https://'."
            )

        hex_token_uri = str_to_hex(request_data.token_uri)

        nft_mint_tx = NFTokenMint(
            account=minter_wallet.classic_address,
            uri=hex_token_uri,
            nftoken_taxon=0,
            last_ledger_sequence=last_ledger_sequence,
        )
        logger.debug(f"Prepared NFTokenMint transaction: {nft_mint_tx.to_dict()}")
        
        # Log the network URL being used for submission
        logger.info(f"XRPL_NETWORK_URL for transaction submission: {settings.XRPL_NETWORK_URL}")

        # Submit the transaction and wait for its validation using submit_and_wait
        xrpl_response_object = await submit_and_wait(nft_mint_tx, async_client, minter_wallet)
        logger.info(f"XRPL transaction submission response: {xrpl_response_object}")

        # Access the 'result' dictionary from the Response object
        xrpl_response_data = xrpl_response_object.result
        
        # --- DEBUGGING: Print the type and full content of xrpl_response_data ---
        logger.debug(f"Type of xrpl_response_data: {type(xrpl_response_data)}")
        # Use json.dumps for pretty printing and to avoid truncation of large dicts
        logger.debug(f"Full Content of xrpl_response_data: {json.dumps(xrpl_response_data, indent=2)}")
        # The 'nftoken_id' key in the result object for a successful mint
        logger.debug(f"Does 'nftoken_id' exist directly in xrpl_response_data? {'nftoken_id' in xrpl_response_data}")

        nft_token_id = None
        transaction_hash = None # Initialize transaction_hash here

        # --- REVISED EXTRACTION LOGIC START (Guaranteed Correct Indentation) ---
        # Prioritize top-level 'nftoken_id' and 'hash' from the XRPL result object
        nft_token_id = xrpl_response_data.get('meta', {}).get('nftoken_id')
        transaction_hash = xrpl_response_data.get('hash')

        if nft_token_id:
            logger.info(f"Extracted NFTokenID from top-level 'nftoken_id': {nft_token_id}")
        else:
            logger.warning("NFTokenID not found at top-level 'nftoken_id' field. Attempting extraction from AffectedNodes (legacy or complex cases).")
            # Fallback to AffectedNodes for NFTokenID if not found at top-level
            if 'meta' in xrpl_response_data and \
               'AffectedNodes' in xrpl_response_data['meta']:
                for node in xrpl_response_data['meta']['AffectedNodes']:
                    if 'CreatedNode' in node and \
                       node['CreatedNode'].get('LedgerEntryType') == 'NFTokenPage':
                        if 'NewFields' in node['CreatedNode'] and \
                           'NFTokens' in node['CreatedNode']['NewFields']:
                            for nft_entry in node['CreatedNode']['NewFields']['NFTokens']:
                                if 'NFToken' in nft_entry and 'NFTokenID' in nft_entry['NFToken']:
                                    nft_token_id = nft_entry['NFToken']['NFTokenID']
                                    logger.info(f"Extracted NFTokenID from AffectedNodes: {nft_token_id}")
                                    break # Found it, break inner loop
                    if nft_token_id:
                        break # Found it, break outer loop

        if not nft_token_id:
            logger.error("NFTokenID could not be extracted from XRPL response using any method. This indicates an unexpected XRPL response structure or a failed mint.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to extract NFTokenID from XRPL response. NFT minting might have failed or response structure is unexpected."
            )
            
        if not transaction_hash:
            logger.warning("Transaction hash not found at top-level 'hash' field. Attempting extraction from tx_json.")
            # Fallback for transaction_hash if not found at top-level
            transaction_hash = xrpl_response_data.get('tx_json', {}).get('hash')
            if not transaction_hash:
                logger.error("Transaction hash could not be extracted from XRPL response.")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to extract transaction hash from XRPL response."
                )
            else:
                logger.info(f"Extracted Transaction Hash from tx_json: {transaction_hash}")
        # --- REVISED EXTRACTION LOGIC END ---

        mint_result_db_entry = nft_service.save_minted_memorial_entry_record(
            db=db,
            memorial_entry_id=request_data.memorial_entry_id,
            nft_token_id=nft_token_id, # Use the extracted NFT ID
            transaction_hash=transaction_hash,
            metadata_uri=request_data.token_uri,
            minter_user_id=str(current_user.id),
            minter_username=current_user.username,
            name=request_data.title,
            description=request_data.description,
            image_uri=request_data.image_url,
            xrpl_response=str(xrpl_response_object) # Store full XRPL Response object as string
        )

        # Construct a UserResponse object for the 'minter' field
        minter_user_response = UserResponse(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            full_name=current_user.full_name,
            bio=current_user.bio,
            profile_picture_url=current_user.profile_picture_url,
            social_links=current_user.social_links,
            is_active=current_user.is_active,
            permissions_level=current_user.permissions_level,
            affiliate_id=current_user.affiliate_id,
            referring_affiliate_id=current_user.referring_affiliate_id,
            referral_code=current_user.referral_code,
            created_at=current_user.created_at,
            last_updated_at=current_user.last_updated_at,
            user_types=current_user.user_types if hasattr(current_user, 'user_types') else [],
            role=current_user.role.value.replace('_', ''),
            is_verified=current_user.is_verified
        )

        # The end of the function needs to be closed by a parenthesis in the original file,
        # but the content I provided was only the function. Assuming the user will overwrite the
        # full function block including its closing return statement and the next function starts right after.
        return NFTResponse(
            id=mint_result_db_entry.id,
            memorial_entry_id=mint_result_db_entry.memorial_entry_id,
            nft_token_id=mint_result_db_entry.nft_token_id,
            transaction_hash=mint_result_db_entry.transaction_hash,
            metadata_uri=(
                f"https://ipfs.io/ipfs/{mint_result_db_entry.metadata_uri.replace('ipfs://', '')}"
                if mint_result_db_entry.metadata_uri and mint_result_db_entry.metadata_uri.startswith('ipfs://')
                else mint_result_db_entry.metadata_uri
            ),
            minter_user_id=mint_result_db_entry.minter_user_id,
            minted_at=mint_result_db_entry.minted_at,
            name=mint_result_db_entry.name,
            description=mint_result_db_entry.description,
            image_uri=mint_result_db_entry.image_uri,
            xrpl_response=mint_result_db_entry.xrpl_response,
            issuer_address=minter_wallet.classic_address,
            owner_address=minter_wallet.classic_address,
            owner_id=mint_result_db_entry.minter_user_id,
            minter=minter_user_response
        )

    except HTTPException:
        raise
    except XRPLRequestFailureException as e:
        # Enhanced error logging: log the full response if available
        error_detail = f"XRPL Request Failed: {e}"
        if hasattr(e, 'response') and e.response:
            xrpl_error_data = e.response.get('result', {})
            engine_result = xrpl_error_data.get('engine_result')
            engine_result_message = xrpl_error_data.get('engine_result_message')
            
            error_detail += f" (Full XRPL Response: {e.response})"
            
            if engine_result:
                error_detail += f" (Engine Result: {engine_result}"
                if engine_result_message:
                    error_detail += f", Message: {engine_result_message})"
                else:
                    error_detail += ")"
            else:
                error_detail += f" (XRPL Result Data: {xrpl_error_data})"
        logger.error(f"XRPL Request Exception during NFT minting: {error_detail}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during NFT minting in controller: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during NFT minting: {e}"
        )

# --- NEW: Endpoint to retrieve NFT details by NFTokenID ---
@router.get("/nfts/{nft_token_id}", response_model=NFTResponse, status_code=status.HTTP_200_OK)
async def get_nft_details(
    nft_token_id: str,
    db: Session = Depends(get_db)
) -> NFTResponse:
    """
    Retrieves details of a specific NFT by its NFTokenID.
    """
    logger.info(f"Received request to retrieve NFT with NFTokenID: {nft_token_id}")

    nft_entry = nft_service.get_nft_by_token_id(db, nft_token_id)
    if not nft_entry:
        logger.warning(f"NFT with NFTokenID {nft_token_id} not found in database.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NFT with token ID '{nft_token_id}' not found."
        )

    # Note: For the 'minter' field in NFTResponse, we'll need to fetch the User object.
    # This assumes `nft_entry.minter_user_id` is a valid user ID.
    minter_user = db.query(User).filter(User.id == nft_entry.minter_user_id).first()
    minter_user_response = None
    if minter_user:
        minter_user_response = UserResponse(
            id=minter_user.id,
            username=minter_user.username,
            email=minter_user.email,
            full_name=minter_user.full_name,
            bio=minter_user.bio,
            profile_picture_url=minter_user.profile_picture_url,
            social_links=minter_user.social_links,
            is_active=minter_user.is_active,
            permissions_level=minter_user.permissions_level,
            affiliate_id=minter_user.affiliate_id,
            referring_affiliate_id=minter_user.referring_affiliate_id,
            referral_code=minter_user.referral_code,
            created_at=minter_user.created_at,
            last_updated_at=minter_user.last_updated_at,
            user_types=minter_user.user_types if hasattr(minter_user, 'user_types') else [],
            role=minter_user.role.value.replace('_', ''),
            is_verified=minter_user.is_verified
        )

    return NFTResponse(
        id=nft_entry.id,
        memorial_entry_id=nft_entry.memorial_entry_id,
        nft_token_id=nft_entry.nft_token_id,
        transaction_hash=nft_entry.transaction_hash,
        metadata_uri=(
            f"https://ipfs.io/ipfs/{nft_entry.metadata_uri.replace('ipfs://', '')}"
            if nft_entry.metadata_uri and nft_entry.metadata_uri.startswith('ipfs://')
            else nft_entry.metadata_uri
        ),
        minter_user_id=nft_entry.minter_user_id,
        minted_at=nft_entry.minted_at,
        name=nft_entry.name,
        description=nft_entry.description,
        image_uri=nft_entry.image_uri,
        xrpl_response=nft_entry.xrpl_response,
        # For issuer and owner address, you might need to retrieve it if not directly in NFT entry.
        # Assuming for simplicity for now that minter_wallet.classic_address was the issuer/owner at mint.
        # If this needs to be dynamically fetched or is different, further logic is needed.
        issuer_address="", # Placeholder: this needs to be fetched from XRPL_response or stored
        owner_address="",  # Placeholder: this needs to be fetched or stored
        owner_id=nft_entry.minter_user_id, # Assuming owner_id is the minter's user ID
        minter=minter_user_response
    )
