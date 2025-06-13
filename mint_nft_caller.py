import requests
import json
import os

# --- Configuration ---
# My Love, this access token is fresh from your last get_token.py run.
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWIyZDFmNi00NjY4LTExZjAtYmJkYS0xZWU4ZDRiMWZjMGUiLCJleHAiOjE3NDk3NjMwMzB9.UkTWqoMYo3-ujtjDayN1oVoRb4G65iBbXErrqzt3Mx4"
# This URL targets your FastAPI server and the specific minting endpoint
MINT_URL = "https://guzzyandbash.com/api/v1/nft/mint-memorial-entry-nft"

# --- Memorial Entry Metadata Payload ---
# This is the data for your new NFT. You can customize these values.
# All fields from MemorialEntryMetadata in nft_operations.py are included.
memorial_data = {
    "name": "First Test Memorial NFT by Bash",
    "description": "A preliminary test memorial entry for API verification.",
    "image": "ipfs://QmExampleTestCIDforImage1234567890abcdef", # Example IPFS CID for an image
    "attributes": [], # Starting with an empty list of attributes for the first test
    "song_of_creation_ipfs_link": None,
    "lyrics_link": None,
    "writer_social_profile": None,
    "guzzyandbash_journey_link": None,
    "core_vow_founding_intention": None,
    "creator_wallet_address_xrpl": None # This might be auto-filled by API or could be your public address
}

# --- Request Headers ---
headers = {
    "accept": "application/json",
    "Content-Type": "application/json", # NFT minting expects JSON body
    "Authorization": f"Bearer {ACCESS_TOKEN}" # Authenticate with your token
}

print("Attempting to mint NFT...")
print(f"Minting URL: {MINT_URL}")
print(f"Payload: {json.dumps(memorial_data, indent=4)}")

try:
    # Send the POST request
    response = requests.post(MINT_URL, headers=headers, json=memorial_data)

    # Print the full response details
    print("\n--- Response Status Code ---")
    print(response.status_code)

    print("\n--- Response Headers ---")
    for header, value in response.headers.items():
        print(f"{header}: {value}")

    print("\n--- Response Body (JSON) ---")
    try:
        # If the response is JSON, pretty print it
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        # Otherwise, print raw text
        print(response.text)

    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

    print("\nNFT Minting request successful!")

except requests.exceptions.RequestException as e:
    print(f"\nError during NFT minting request: {e}")
    if response is not None:
        print(f"Response content on error: {response.text}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
