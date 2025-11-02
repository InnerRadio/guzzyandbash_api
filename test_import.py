import sys
import os
from pathlib import Path

# Set up sys.path to mimic the application's root directory for imports
# Assuming this script is run from /var/www/guzzyandbash_app
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT)) # Insert at the beginning to prioritize local imports

print(f"sys.path: {sys.path}")
print(f"os.getcwd(): {os.getcwd()}")

try:
    from app.schemas.user_schemas import NFTResponse
    print("Successfully imported NFTResponse!")
    # You can uncomment the line below to see the schema's properties
    # print(NFTResponse.model_json_schema())
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")