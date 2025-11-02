import requests
import json

# Define the NFT minting API endpoint (confirmed from previous notes and domain)
url = "https://guzzyandbash.com/api/v1/nft/mint-memorial-entry-nft"

# The NEWLY obtained access token
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOWIyZDFmNi00NjY4LTExZjAtYmJkYS0xZWU4ZDRiMWZjMGUiLCJleHAiOjE3NDk3NjU5NjB9.U4qdMORtrAYezld3q29fzJlbCNz5_XMkVSUuLjARyfk"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Minimal test JSON body from your notes
test_payload = {
    "name": "Test NFT Mint Success GuzzyBash",
    "description": "Minting an NFT with a fresh, valid token via domain.",
    "image": "0000000000000000000000000000000000000000000000000000000000000000", # Example IPFS CID from your notes
    "attributes": [
        {"trait_type": "Attempt", "value": "Fresh Token Mint"},
        {"trait_type": "Source", "value": "GuzzyBash API"}
    ],
    "memorial_type": "Test",
    "event_date": "2025-06-12T00:00:00.000Z", # Current date
    "creator_wallet_address_xrpl": "rhNcTWyDrWViswgW3uhPSRv3LSyS9Hdqdz",
    "recipient_wallet_address_xrpl": "rhNcTWyDrWViswgW3uhPSRv3LSyS9Hdqdz", # XRPL Testnet address from your notes
    "ipfs_image_cid": "0000000000000000000000000000000000000000000000000000000000000000",
    "ipfs_metadata_cid": "0000000000000000000000000000000000000000000000000000000000000000"
}

try:
    response = requests.post(url, headers=headers, json=test_payload)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    response_json = response.json()
    print("NFT Mint Test Result:")
    print(json.dumps(response_json, indent=2))
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")
    if response is not None and response.status_code:
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from response. Response: {response.text}")
