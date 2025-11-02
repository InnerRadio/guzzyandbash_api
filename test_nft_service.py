# /var/www/guzzyandbash_app/test_nft_service.py

import sys
import os
import asyncio
import logging

# Configure logging to show DEBUG messages to stderr for this script
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr,
                    format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

# Add the application root to sys.path to ensure 'app' package is discoverable
# This mimics how a web server might set up the path.
app_root = "/var/www/guzzyandbash_app"
if app_root not in sys.path:
    sys.path.insert(0, app_root)

logger.debug(f"DEBUG: test_nft_service.py is running from: {__file__}")
logger.debug(f"DEBUG: Python sys.path for test script: {sys.path}")
logger.debug(f"DEBUG: Current working directory for test script: {os.getcwd()}")

# Import nft_service after setting up sys.path
try:
    from app.services import nft_service
    logger.debug(f"DEBUG: Successfully imported app.services.nft_service from: {nft_service.__file__}")
except ImportError as e:
    logger.error(f"ERROR: Failed to import app.services.nft_service: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"ERROR: An unexpected error during nft_service import: {e}")
    sys.exit(1)

# Dummy SessionLocal for testing purposes (not a real DB session)
class MockDBSession:
    def close(self):
        logger.info("Mock DB Session closed.")

async def run_test():
    logger.info("Starting isolated NFT minting test...")

    # Use the wallet seed from the environment variable if available, otherwise a dummy
    wallet_seed = os.getenv("XRPL_WALLET_SEED", "sEdVMy62S9vV91Wuide8FXQFekCueyn")

    # Call the create_minted_memorial_entry function directly
    try:
        result = await nft_service.create_minted_memorial_entry(
            db=MockDBSession(), # Pass a mock DB session
            memorial_entry_id="test-isolated-entry-001",
            token_uri="ipfs://bafybeigdyrzt5gqf34nm42l4r5e4c63673w222w222w222w222w222",
            category="Human",
            minter_user_id="isolated_test_user_id",
            minter_username="isolated_test_user",
            wallet_seed=wallet_seed
        )
        logger.info(f"Isolated NFT minting test successful: {result}")
    except Exception as e:
        logger.error(f"Isolated NFT minting test failed with error: {e}", exc_info=True)

if __name__ == "__main__":
    # Ensure the virtual environment's site-packages are on sys.path
    # This is usually handled by 'source venv/bin/activate' but good to double check
    # for isolated script execution.
    venv_site_packages = os.path.join(app_root, 'venv', 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
    if venv_site_packages not in sys.path:
        sys.path.insert(0, venv_site_packages)
    
    # Run the async test function
    asyncio.run(run_test())
    logger.info("Isolated NFT minting test finished.")

