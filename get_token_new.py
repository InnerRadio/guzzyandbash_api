import requests
import json

# Define the API endpoint based on your confirmed details
url = "https://guzzyandbash.com/api/auth/token"

# Define the credentials
username = "guzzy_superuser"
password = "GuzzyBash#@!9"

# Prepare the form data as x-www-form-urlencoded
data = {
    "username": username,
    "password": password
}

headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    response_json = response.json()
    if "access_token" in response_json:
        print(f"New JWT Token: {response_json['access_token']}")
    else:
        print("Error: 'access_token' not found in the response.")
        print(f"Full API Response: {response_json}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")
    if response is not None and response.status_code:
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from response. Response: {response.text}")
