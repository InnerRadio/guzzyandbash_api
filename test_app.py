# /var/www/guzzyandbash_app/test_app.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import logging
import os

# Define the log file path
LOG_FILE = "/var/www/guzzyandbash_app/logs/test_app_debug.log"

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure a logger for this test app to write to a file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Set logging level to DEBUG

# Create a file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Optionally, remove any default handlers that might be causing issues (like StreamHandler)
# for handler in logging.root.handlers[:]:
#     logging.root.removeHandler(handler)


app = FastAPI(title="Minimal Test API")

@app.post("/token")
async def test_token_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    A minimal endpoint to test OAuth2PasswordRequestForm parsing.
    """
    logger.debug(f"Received username: {form_data.username}")
    logger.debug(f"Received password: {form_data.password}")
    return {"message": "Form data received successfully!", "username": form_data.username}

@app.on_event("startup")
async def startup_event():
    logger.info("Minimal Test App started up.")
