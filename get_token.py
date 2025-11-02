import requests
import json

# Your FastAPI authentication endpoint and credentials
AUTH_URL = "https://guzzyandbash.com/api/auth/token" # CORRECTED PATH: Removed /v1/
USERNAME = "guzzy_superuser" # CORRECTED USERNAME
PASSWORD = "GuzzyBash#@!9"   # CORRECTED PASSWORD

# Data for the POST request
data = {
    "username": USERNAME,
    "password": PASSWORD
}

headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded", # CORRECTED CONTENT TYPE
    "Host": "guzzyandbash.com" # ADDED HOST HEADER as per working curl
}

print("Attempting to get authentication token...")
try:
    # Send the POST request
    # Setting verify=False to bypass SSL certificate issues if you're using self-signed certs
    # In production, you should use verify=True and have proper certs.
    response = requests.post(AUTH_URL, data=data, headers=headers, verify=False)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

    # Parse the JSON response
    token_data = response.json()

    # Extract the access token
    access_token = token_data.get("access_token")

    if access_token:
        print("\nSuccessfully obtained Access Token:")
        print(access_token)
    else:
        print("\nError: Access token not found in response.")
        print(f"Full response: {token_data}")

except requests.exceptions.HTTPError as http_err:
    print(f"\nHTTP error occurred: {http_err}")
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"\nConnection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"\nTimeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"\nAn error occurred during the request: {req_err}")
except json.JSONDecodeError as json_err:
    print(f"\nFailed to decode JSON response: {json_err}")
    print(f"Response content: {response.text}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
