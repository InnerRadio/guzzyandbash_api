# app/xrpl/wallet.py
# This file contains utility functions for interacting with the XRP Ledger (XRPL),
# specifically for submitting signed transactions.

# Standard library imports
import logging
from typing import Dict, Any, Optional
import asyncio # New import for asyncio.to_thread

# XRPL.py library imports
from xrpl.clients import JsonRpcClient
from xrpl.models import Response
from xrpl.transaction import submit_and_wait # For submitting signed transactions and waiting for result
from xrpl.wallet import Wallet # For creating Wallet objects from seeds (for testing/internal use)

# Application configuration imports
from app.config import settings

# Configure logging for this module
logger = logging.getLogger(__name__)

# Global client initialization (needed for get_latest_validated_ledger_sequence in nft_operations.py)
# This client will be used for network queries that are not part of the blocking submit_and_wait.
client = JsonRpcClient(settings.XRPL_NETWORK_URL)

def get_testnet_wallet(seed: str, app_settings: Any) -> Wallet:
    """
    Creates an XRPL Wallet object from a given seed.
    WARNING: This function exposes the seed directly. It is intended for
    TESTNET development and internal G&B Productions treasury operations
    (where a secure signing service will abstract seed handling).
    NEVER use this with production/mainnet seeds in a publicly accessible API.

    Args:
        seed (str): The secret seed for the wallet.
        app_settings (Any): The application settings object, containing XRPL_WALLET_SEED.
    """
    logger.debug(f"Creating XRPL Wallet from seed (TESTNET/internal use only).")
    try:
        wallet = Wallet.from_seed(seed)
        logger.info(f"Testnet Wallet created with public address: {wallet.classic_address}")
        return wallet
    except Exception as e:
        logger.error(f"Error creating wallet from seed: {e}", exc_info=True)
        raise

# NEW: Synchronous helper function to run in a separate thread
def _submit_transaction_sync(signed_tx_blob: str, current_client: JsonRpcClient) -> Response:
    """
    Synchronously submits a signed XRPL transaction blob to the ledger and waits for its result.
    This function is designed to be run in a separate thread.
    """
    logger.debug("Running _submit_transaction_sync in a separate thread.")
    # Ensure the client is connected within this thread's context if it's not already
    # (JsonRpcClient handles connection pooling and re-connection internally)
    return submit_and_wait(signed_tx_blob, current_client)

async def submit_transaction(signed_tx_blob: str) -> Dict[str, Any]:
    """
    Submits a signed XRPL transaction blob to the ledger and waits for its result.
    This function is generic and can be used for any signed transaction (e.g., NFT mint, LV8 transfer).

    Args:
        signed_tx_blob (str): The signed transaction in hexadecimal blob format.

    Returns:
        Dict[str, Any]: A dictionary containing the transaction result,
                        including the transaction hash and ledger response.

    Raises:
        Exception: If the transaction submission fails or the response indicates an error.
    """
    logger.info(f"Attempting to submit signed XRPL transaction using asyncio.to_thread.")
    try:
        # Use asyncio.to_thread to run the synchronous _submit_transaction_sync in a separate thread.
        # This completely isolates its execution from the main event loop.
        response: Response = await asyncio.to_thread(
            _submit_transaction_sync,
            signed_tx_blob,
            client # Pass the global client to the synchronous helper
        )

        # Check if the transaction was successful on the ledger
        # The 'result' field of the response contains the transaction outcome.
        # 'tesSUCCESS' indicates a successful transaction.
        if response.result['meta']['TransactionResult'] == 'tesSUCCESS':
            logger.info(f"XRPL transaction successful. Transaction Hash: {response.result['hash']}")
            return {
                "transaction_hash": response.result['hash'],
                "ledger_index": response.result['ledger_index'],
                "result_code": response.result['meta']['TransactionResult'],
                "full_response": response.result
            }
        else:
            # Log and raise an error if the transaction failed on the ledger
            error_message = (
                f"XRPL transaction failed. Result: {response.result['meta']['TransactionResult']} "
                f"Hash: {response.result['hash']} "
                f"Error: {response.result.get('meta', {}).get('Error')}"
            )
            logger.error(error_message)
            raise Exception(f"XRPL transaction failed: {response.result['meta']['TransactionResult']}")

    except Exception as e:
        logger.error(f"Error submitting XRPL transaction: {e}", exc_info=True)
        # Re-raise the exception to be handled by the calling function/endpoint
        raise
