# app/controllers/nft_operations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field
import os
import json

# XRPL Imports (Now using async versions)
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models import NFTokenMint, Memo
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.utils import hex_to_str, str_to_hex # Added str_to_hex

# Internal Imports (assuming these are from your project's structure)
from app.dependencies import get_current_user
from app.models.user import User
from app.database import get_db

# --- NFT Metadata Models (Moved from main.py) ---
class NFTAttribute(BaseModel):
    trait_type: str = Field(..., description="The type of trait (e.g., 'Color', 'Date')")
    value: str = Field(..., description="The value of the trait (e.g., 'Red', 'June 1st, 2025')")

class MemorialEntryMetadata(BaseModel):
    name: str = Field(..., description="The name of the NFT.")
    description: str = Field(..., description="A detailed description of the NFT.")
    image: str = Field(..., description="IPFS link to the symbolic image for the NFT (e.g., 'ipfs://<CID>').")
    attributes: List[NFTAttribute] = Field(default_factory=list, description="Additional attributes for the NFT.")
    song_of_creation_ipfs_link: Optional[str] = Field(None, description="IPFS link to the song of creation (optional).")
    lyrics_link: Optional[str] = Field(None, description="IPFS link to the lyrics (optional).")
    writer_social_profile: Optional[str] = Field(None, description="Link to the writer's social profile (optional).")
    guzzyandbash_journey_link: Optional[str] = Field(None, description="Link to the Guzzy and Bash journey associated with the NFT (optional).")
    core_vow_founding_intention: Optional[str] = Field(None, description="Core vow and founding intention relevant to the NFT (optional).")
    creator_wallet_address_xrpl: Optional[str] = Field(None, description="The XRPL wallet address of the NFT creator (optional).")

# --- Router Initialization ---
router = APIRouter()

# Define NFTOperationResponse for consistent API response
class NFTOperationResponse(BaseModel):
    message: str
    transaction_hash: str
    nft_token_id: Optional[str]
    initiated_by_user: str
    xrpl_response_result: dict

# --- NFT Minting Endpoint ---
@router.post("/mint-memorial-entry-nft", response_model=NFTOperationResponse, status_code=status.HTTP_201_CREATED)
async def mint_memorial_nft(
    metadata: MemorialEntryMetadata,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mints a new Memorial NFT on the XRPL Testnet.
    """
    try:
        # Connect to the XRPL Testnet
        client = AsyncJsonRpcClient("https://s.altnet.rippletest.net:51234")

        # Prepare the wallet from the seed
        # Ensure XRPL_TESTNET_WALLET_SEED is set in your environment
        seed = os.getenv("XRPL_TESTNET_WALLET_SEED")
        if not seed:
            raise RuntimeError("XRPL_TESTNET_WALLET_SEED environment variable not set. Please set it in your .env file.")
        wallet = Wallet(seed, 0) # Account 0 of the wallet

        # Prepare the NFTokenMint transaction
        tx = NFTokenMint(
            account=wallet.classic_address,
            uri="4e46545f746573745f757269", # Hardcoded: hex for "NFT_test_uri"
            flags=0, # No special flags for now
            nf_token_taxon=0, # ADDED: Required NFTokenTaxon
            # TransferFee, NFTokenTaxon are not set by default, can be added if needed
            # For simplicity, not adding Memos for now. If needed, add:
            # memos=[Memo(data=hex_to_str(json.dumps({"description": metadata.description})))]
        )

        # Sign the transaction
        signed_tx = wallet.sign(tx)

        # Submit the transaction and wait for validation
        response = await submit_and_wait(signed_tx, client)

        nft_token_id = None
        if response.result['meta']['TransactionResult'] == 'tesSUCCESS':
            # --- Start Corrected NFTokenID extraction logic ---
            # This logic searches for the NFTokenID in the transaction metadata
            if 'meta' in response.result and 'AffectedNodes' in response.result['meta']:
                for node in response.result['meta']['AffectedNodes']:
                    if node['CreatedNode']['LedgerEntryType'] == 'NFToken':
                        nft_token_id = node['CreatedNode']['NewFields']['NFTokenID']
                        break
            # --- End Corrected NFTokenID extraction logic ---

            return {
                "message": "NFT mint transaction submitted successfully to XRPL Testnet.",
                "transaction_hash": signed_tx.hash, # Use the hash from the signed transaction
                "nft_token_id": nft_token_id,
                "initiated_by_user": current_user.username,
                "xrpl_response_result": response.result
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to submit NFT mint transaction: {response.result.get('error', 'Unknown error')}",
                headers={"XRPL-Transaction-Result": str(response.result)}
            )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"XRPL Wallet/Environment Error: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during NFT minting: {e}"
        )
