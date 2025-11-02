#!/bin/bash

# This script focuses on testing the Authentication and User Profile endpoints.
# It automatically logs in as a superuser to obtain a fresh access token.

# --- Configuration ---
API_BASE_URL="https://guzzyandbash.com"
SUPERUSER_USERNAME="guzzy_superuser"
SUPERUSER_PASSWORD="GuzzyBash#@!9"

# --- Colors for better output visibility ---
GREEN='\033[0;32m'
YELLOW='\033;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Global variables for dynamic data ---
ACCESS_TOKEN=""
SUPERUSER_ID=""

# --- Function to print section headers ---
print_header() {
    echo -e "\n${YELLOW}--- $1 ---${NC}"
}

# --- Function to make authenticated GET requests ---
make_authenticated_get_request() {
    local endpoint="$1"
    local token="$2"
    print_header "Testing GET $endpoint"
    if [ -z "$token" ]; then
        echo -e "${RED}ERROR: No access token available for authenticated request.${NC}"
        echo -e "HTTP Status: N/A"
        echo -e "${RED}FAILED: GET $endpoint${NC}"
        return 1
    fi
    response=$(curl -s -w "\nHTTP Status: %{http_code}\n" -H "Authorization: Bearer $token" "$API_BASE_URL$endpoint")
    echo "$response"
    # Check if the response contains "HTTP Status: 200"
    if echo "$response" | grep -q "HTTP Status: 200"; then
        echo -e "${GREEN}SUCCESS: GET $endpoint${NC}"
        return 0
    else
        echo -e "${RED}FAILED: GET $endpoint${NC}"
        return 1
    fi
}

# --- Main Test Execution ---

print_header "Step 1: Attempting to log in as superuser to obtain token..."
LOGIN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$SUPERUSER_USERNAME&password=$SUPERUSER_PASSWORD" \
  -w "\nHTTP Status: %{http_code}\n" \
  "$API_BASE_URL/api/auth/token")

# Echo the raw login response for debugging
echo "$LOGIN_RESPONSE"

# Extract access token
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d':' -f2 | tr -d '"')

if [ -z "$ACCESS_TOKEN" ]; then
    echo -e "${RED}ERROR: Failed to obtain access token. Cannot proceed with authenticated tests.${NC}"
    exit 1
else
    echo -e "${GREEN}SUCCESS: Access token obtained.${NC}"
fi

# --- Authentication & Users Endpoints ---
print_header "Testing Authentication & Users Endpoints"

# Test GET /api/auth/users/me
ME_RESPONSE=$(make_authenticated_get_request "/api/auth/users/me" "$ACCESS_TOKEN")
if [ $? -eq 0 ]; then
    # Extract superuser ID from the /me response
    SUPERUSER_ID=$(echo "$ME_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d':' -f2 | tr -d '"')
    if [ -n "$SUPERUSER_ID" ]; then
        echo -e "${BLUE}Superuser ID obtained: $SUPERUSER_ID${NC}"
        # Test GET /api/auth/users/{user_id} using the extracted ID
        make_authenticated_get_request "/api/auth/users/$SUPERUSER_ID" "$ACCESS_TOKEN"
    else
        echo -e "${RED}ERROR: Could not extract Superuser ID for /api/auth/users/{user_id} test.${NC}"
    fi
else
    echo -e "${RED}Skipping /api/auth/users/{user_id} test due to /api/auth/users/me failure.${NC}"
fi

echo -e "\n${YELLOW}--- Authentication & Users Endpoints Tests Completed ---${NC}"
