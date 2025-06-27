# app/controllers/nft_operations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from typing import Optional, List
from pydantic import BaseModel, Field
import os
import json
import logging

# Configure logging (for standard FastAPI/Uvicorn logs)
logging.basicConfig(level=logging.INFO) # Changed to INFO for production-level logging
logger = logging.getLogger(__name__)

# XRPL Imports
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models import NFTokenMint, Memo
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.utils import hex_to_str, str_to_hex

# Internal Imports
from app.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.nft import MintedMemorialEntry, MintedMemorialEntryResponse
from app.database import get_db

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


# --- Helper Function to Extract NFTokenID ---
def extract_nft_token_id(response: dict) -> Optional[str]:
    """
    Extracts the NFTokenID from various possible locations within the XRPL transaction response.
    """
    logger.info(f"Full XRPL response.result in extract_nft_token_id: {json.dumps(response, indent=2)}")

    # Attempt 1: Check for 'nftoken_id' directly in meta
    if 'meta' in response and isinstance(response['meta'], dict):
        if 'nftoken_id' in response['meta']:
            logger.debug(f"Found NFTokenID in meta.nftoken_id: {response['meta']['nftoken_id']}")
            return response['meta']['nftoken_id']

    # Attempt 2: Check for 'NFTokenID' in the AffectedNodes
    if 'meta' in response and isinstance(response['meta'], dict) and 'AffectedNodes' in response['meta']:
        for node in response['meta']['AffectedNodes']:
            if 'ModifiedNode' in node and 'FinalFields' in node['ModifiedNode']:
                final_fields = node['ModifiedNode']['FinalFields']
                if 'NFTokens' in final_fields:
                    for nftoken_entry in final_fields['NFTokens']:
                        if 'NFToken' in nftoken_entry and 'NFTokenID' in nftoken_entry['NFToken']:
                            logger.debug(f"Found NFTokenID in AffectedNodes: {nftoken_entry['NFToken']['NFTokenID']}")
                            return nftoken_entry['NFToken']['NFTokenID']
            if 'CreatedNode' in node and 'NewFields' in node['CreatedNode']:
                new_fields = node['CreatedNode']['NewFields']
                if 'NFTokenID' in new_fields:
                    logger.debug(f"Found NFTokenID in CreatedNode: {new_fields['NFTokenID']}")
                    return new_fields['NFTokenID']

    # Attempt 3: Check for 'NFTokenID' in the top-level response.result
    if 'NFTokenID' in response:
        logger.debug(f"Found NFTokenID at top level of response.result: {response['NFTokenID']}")
        return response['NFTokenID']

    # Attempt 4: Check for 'NFTokenID' directly under response.result.meta for older or different structures
    if 'meta' in response and isinstance(response['meta'], dict) and 'NFTokenID' in response['meta']:
        logger.debug(f"Found NFTokenID in response.result.meta: {response['meta']['NFTokenID']}")
        return response['meta']['NFTokenID']

    logger.debug("NFTokenID not found in response metadata after checking all nodes.")
    return None

# --- APIRouter setup ---
router = APIRouter()

# --- Endpoint to mint a memorial entry NFT ---
@router.post("/mint-memorial-entry-nft", status_code=status.HTTP_200_OK)
async def mint_memorial_entry_nft(
    request: MintMemorialEntryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check for existing entry to prevent duplicate minting for the same memorial_entry_id
    existing_entry = db.execute(
        select(MintedMemorialEntry).filter_by(memorial_entry_id=request.memorial_entry_id)
    ).scalar_one_or_none()

    if existing_entry:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An NFT for memorial entry ID '{request.memorial_entry_id}' has already been minted. Transaction Hash: {existing_entry.transaction_hash}, NFTokenID: {existing_entry.nft_token_id}",
        )

    # Role check
    if current_user.role not in [UserRole.ADMIN, UserRole.CREATOR, UserRole.SUPER_USER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin, creator, or super user roles can mint NFTs."
        )

    try:
        # Connect to XRPL Testnet
        json_rpc_url = os.getenv("XRPL_JSON_RPC_URL", "https://s.altnet.rippletest.net:51234/")
        client = AsyncJsonRpcClient(json_rpc_url)

        # Prepare wallet from seed.
        wallet = Wallet.from_seed(request.wallet_seed)

        logger.debug(f"Wallet address: {wallet.classic_address}")

        # Convert token_uri and memo data to hex
        uri_hex = str_to_hex(request.token_uri)
        memorial_entry_id_memo_hex = str_to_hex(f"MemorialEntryID:{request.memorial_entry_id}")
        category_memo_hex = str_to_hex(f"Category:{request.category}")

        # Prepare transaction with Memos
        memos = [
            Memo(memo_data=memorial_entry_id_memo_hex, memo_format=str_to_hex("text/plain")),
            Memo(memo_data=category_memo_hex, memo_format=str_to_hex("text/plain"))
        ]

        transaction = NFTokenMint(
            account=wallet.classic_address,
            uri=uri_hex,
            flags=0, # Use default flags for simple mint
            nftoken_taxon=0, # A taxon of 0 is common for fungible NFTs or when not using a specific taxon
            memos=memos
        )

        # Sign and submit transaction
        logger.info(f"Submitting NFTokenMint transaction for account: {wallet.classic_address}")
        response = await submit_and_wait(transaction, client, wallet)
        logger.info(f"XRPL transaction response received. Result: {response.result.get('meta', {}).get('TransactionResult', 'No result meta')}")

        if response.result['meta']['TransactionResult'] == 'tesSUCCESS':
            logger.info(f"XRPL transaction response (tesSUCCESS): {json.dumps(response.result, indent=2)}")

            # Extract NFTokenID using the robust helper function
            nft_token_id = extract_nft_token_id(response.result)

            if not nft_token_id:
                logger.error("NFTokenID not found in response metadata.")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="NFT mint transaction succeeded but NFTokenID not found in response metadata. Please check the XRPL Explorer with the transaction hash.",
                    headers={"XRPL-Transaction-Hash": response.result['hash']}
                )

            # Convert URI hex back to string for database storage
            metadata_uri_from_tx = response.result['tx_json'].get('URI', '')
            metadata_uri_for_db = hex_to_str(metadata_uri_from_tx) if metadata_uri_from_tx else request.token_uri
            logger.debug(f"Metadata URI for DB: {metadata_uri_for_db}")

            new_minted_entry = MintedMemorialEntry(
                memorial_entry_id=request.memorial_entry_id,
                nft_token_id=nft_token_id,
                transaction_hash=response.result['hash'],
                metadata_uri=metadata_uri_for_db,
                xrpl_response=json.dumps(response.result),
                minter_user_id=current_user.id
            )
            db.add(new_minted_entry)
            db.commit()
            db.refresh(new_minted_entry)

            return {
                "message": "NFT mint transaction submitted successfully to XRPL Testnet.",
                "transaction_hash": response.result['hash'],
                "nft_token_id": nft_token_id,
                "initiated_by_user": current_user.username,
                "xrpl_response_result": response.result['meta']['TransactionResult']
            }
        else:
            error_detail = response.result.get('meta', {}).get('TransactionResult', response.result.get('error_message', response.result.get('error', 'Unknown error')))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to submit NFT mint transaction to XRPL: {error_detail}",
                headers={"XRPL-Transaction-Result": str(response.result)}
            )

    except RuntimeError as e:
        logger.error(f"XRPL Wallet/Environment Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"XRPL Wallet/Environment Error: {e}"
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during NFT minting: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during NFT minting: {e}"
        )

# --- Endpoint to get all NFTs minted by the current user ---
@router.get("/nfts/my-nfts", response_model=List[MintedMemorialEntryResponse], status_code=status.HTTP_200_OK)
async def get_nfts_by_minter_user(
    current_user: User = Depends(get_current_user), # Requires authentication
    db: Session = Depends(get_db)
):
    try:
        # Retrieve all NFTs minted by the current user, eagerly load the minter_user relationship
        nfts = db.execute(
            select(MintedMemorialEntry).options(joinedload(MintedMemorialEntry.minter_user)).filter_by(minter_user_id=current_user.id)
        ).scalars().all()

        if not nfts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NFT not found.")
        
        return nfts

    except Exception as e:
        logger.error(f"An error occurred during NFT retrieval for user {current_user.id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred during NFT retrieval: {e}")

# --- Endpoint to get a single NFT by its NFTokenID ---
@router.get("/nfts/{nft_token_id}", response_model=MintedMemorialEntryResponse, status_code=status.HTTP_200_OK)
async def get_nft_by_token_id(
    nft_token_id: str,
    current_user: User = Depends(get_current_user), # Requires authentication
    db: Session = Depends(get_db)
):
    try:
        # Retrieve NFT from database, eagerly load the minter_user relationship
        nft = db.execute(
            select(MintedMemorialEntry).options(joinedload(MintedMemorialEntry.minter_user)).filter_by(nft_token_id=nft_token_id)
        ).scalar_one_or_none()

        if not nft:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NFT not found.")

        # Permissions check: Only ADMIN, SUPER_USER, or the minter_user can view details
        if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_USER] and \
           current_user.id != nft.minter_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this NFT.")

        return nft

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
