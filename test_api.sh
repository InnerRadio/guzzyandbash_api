#!/bin/bash

# This script performs a comprehensive series of curl requests to test
# ALL major endpoints of the Guzzy and Bash Productions API, including
# authentication, user types CRUD, NFT operations, and various reports.

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
TEST_USER_TYPE_ID=""
MINTED_NFT_TOKEN_ID=""

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
    if echo "$response" | grep -q "HTTP Status: 200"; then
        echo -e "${GREEN}SUCCESS: GET $endpoint${NC}"
        return 0
    else
        echo -e "${RED}FAILED: GET $endpoint${NC}"
        return 1
    fi
}

# --- Function to make authenticated POST requests ---
make_authenticated_post_request() {
    local endpoint="$1"
    local token="$2"
    local data="$3"
    print_header "Testing POST $endpoint"
    if [ -z "$token" ]; then
        echo -e "${RED}ERROR: No access token available for authenticated request.${NC}"
        echo -e "HTTP Status: N/A"
        echo -e "${RED}FAILED: POST $endpoint${NC}"
        return 1
    fi
    response=$(curl -s -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $token" \
      -d "$data" \
      -w "\nHTTP Status: %{http_code}\n" \
      "$API_BASE_URL$endpoint")
    echo "$response"
    if echo "$response" | grep -q "HTTP Status: 201" || echo "$response" | grep -q "HTTP Status: 200"; then
        echo -e "${GREEN}SUCCESS: POST $endpoint${NC}"
        echo "$response" # Return response for parsing
        return 0
    else
        echo -e "${RED}FAILED: POST $endpoint${NC}"
        return 1
    fi
}

# --- Function to make authenticated PUT requests ---
make_authenticated_put_request() {
    local endpoint="$1"
    local token="$2"
    local data="$3"
    print_header "Testing PUT $endpoint"
    if [ -z "$token" ]; then
        echo -e "${RED}ERROR: No access token available for authenticated request.${NC}"
        echo -e "HTTP Status: N/A"
        echo -e "${RED}FAILED: PUT $endpoint${NC}"
        return 1
    fi
    response=$(curl -s -X PUT \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $token" \
      -d "$data" \
      -w "\nHTTP Status: %{http_code}\n" \
      "$API_BASE_URL$endpoint")
    echo "$response"
    if echo "$response" | grep -q "HTTP Status: 200"; then
        echo -e "${GREEN}SUCCESS: PUT $endpoint${NC}"
        return 0
    else
        echo -e "${RED}FAILED: PUT $endpoint${NC}"
        return 1
    fi
}

# --- Function to make authenticated DELETE requests ---
make_authenticated_delete_request() {
    local endpoint="$1"
    local token="$2"
    print_header "Testing DELETE $endpoint"
    if [ -z "$token" ]; then
        echo -e "${RED}ERROR: No access token available for authenticated request.${NC}"
        echo -e "HTTP Status: N/A"
        echo -e "${RED}FAILED: DELETE $endpoint${NC}"
        return 1
    fi
    response=$(curl -s -X DELETE \
      -H "Authorization: Bearer $token" \
      -w "\nHTTP Status: %{http_code}\n" \
      "$API_BASE_URL$endpoint")
    echo "$response"
    if echo "$response" | grep -q "HTTP Status: 204"; then
        echo -e "${GREEN}SUCCESS: DELETE $endpoint${NC}"
        return 0
    else
        echo -e "${RED}FAILED: DELETE $endpoint${NC}"
        return 1
    fi
}

# --- Function to make public GET requests (no auth) ---
make_public_get_request() {
    local endpoint="$1"
    print_header "Testing PUBLIC GET $endpoint"
    response=$(curl -s -w "\nHTTP Status: %{http_code}\n" "$API_BASE_URL$endpoint")
    echo "$response"
    if echo "$response" | grep -q "HTTP Status: 200"; then
        echo -e "${GREEN}SUCCESS: PUBLIC GET $endpoint${NC}"
        return 0
    else
        echo -e "${RED}FAILED: PUBLIC GET $endpoint${NC}"
        return 1
    fi
}

# --- Main Test Execution ---

print_header "Step 1: Attempting to log in as superuser..."
LOGIN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$SUPERUSER_USERNAME&password=$SUPERUSER_PASSWORD" \
  -w "\nHTTP Status: %{http_code}\n" \
  "$API_BASE_URL/api/auth/token")

echo "$LOGIN_RESPONSE"

# Extract access token
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d':' -f2 | tr -d '"')

if [ -z "$ACCESS_TOKEN" ]; then
    echo -e "${RED}ERROR: Failed to obtain access token. Cannot proceed with authenticated tests.${NC}"
    exit 1
else
    echo -e "${GREEN}SUCCESS: Access token obtained.${NC}"
fi

# --- Core Endpoint ---
make_public_get_request "/"

# --- Authentication & Users Endpoints ---
print_header "Testing Authentication & Users Endpoints"
make_authenticated_get_request "/api/auth/users/me" "$ACCESS_TOKEN"
if [ $? -eq 0 ]; then
    # Extract superuser ID for /api/auth/users/{user_id} test
    SUPERUSER_ID=$(echo "$response" | grep -o '"id":"[^"]*"' | head -1 | cut -d':' -f2 | tr -d '"')
    if [ -n "$SUPERUSER_ID" ]; then
        echo -e "${BLUE}Superuser ID obtained: $SUPERUSER_ID${NC}"
        make_authenticated_get_request "/api/auth/users/$SUPERUSER_ID" "$ACCESS_TOKEN"
    else
        echo -e "${RED}ERROR: Could not extract Superuser ID for /api/auth/users/{user_id} test.${NC}"
    fi
fi
# Note: POST /api/auth/register is not included for automated testing due to unique credential requirements.

# --- User Types Endpoints (CRUD Sequence) ---
print_header "Testing User Types Endpoints (CRUD Sequence)"

# POST a new User Type Option
TEST_USER_TYPE_NAME="Script Test Type $(date +%s)" # Unique name
CREATE_USER_TYPE_PAYLOAD="{\"name\":\"$TEST_USER_TYPE_NAME\",\"description\":\"Created by automated test script\",\"is_active\":true}"
CREATE_RESPONSE=$(make_authenticated_post_request "/api/v1/user_types/" "$ACCESS_TOKEN" "$CREATE_USER_TYPE_PAYLOAD")
if [ $? -eq 0 ]; then
    TEST_USER_TYPE_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d':' -f2 | tr -d '"')
    echo -e "${BLUE}New User Type ID obtained: $TEST_USER_TYPE_ID${NC}"
    
    # GET all User Type Options (already tested, but re-run to see new one)
    make_authenticated_get_request "/api/v1/user_types/" "$ACCESS_TOKEN"

    # GET User Type Option by ID
    if [ -n "$TEST_USER_TYPE_ID" ]; then
        make_authenticated_get_request "/api/v1/user_types/$TEST_USER_TYPE_ID" "$ACCESS_TOKEN"

        # PUT (Update) the User Type Option
        UPDATE_USER_TYPE_PAYLOAD="{\"name\":\"${TEST_USER_TYPE_NAME} Updated\",\"description\":\"Updated by automated test script\",\"is_active\":false}"
        make_authenticated_put_request "/api/v1/user_types/$TEST_USER_TYPE_ID" "$ACCESS_TOKEN" "$UPDATE_USER_TYPE_PAYLOAD"

        # DELETE the User Type Option
        make_authenticated_delete_request "/api/v1/user_types/$TEST_USER_TYPE_ID" "$ACCESS_TOKEN"
    else
        echo -e "${RED}ERROR: Could not get TEST_USER_TYPE_ID for subsequent User Type tests.${NC}"
    fi
else
    echo -e "${RED}ERROR: Failed to create new User Type for CRUD test.${NC}"
fi


# --- Admin Reports Endpoints ---
print_header "Testing Admin Reports Endpoints"
make_authenticated_get_request "/api/v1/admin_reports/users-summary" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/content-summary" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/users" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/content" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/superuser/reports/token-usage" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/superuser/reports/nft-mint-activity" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/superuser/reports/financial" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/superuser/reports/ipfs-costs" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/superuser/reports/engagement" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/superuser/reports/users-by-referral" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/admin_reports/superuser/reports/affiliate-commissions" "$ACCESS_TOKEN"


# --- Public Reports Endpoints ---
print_header "Testing Public Reports Endpoints"
make_public_get_request "/api/v1/public/reports/top-content"
make_public_get_request "/api/v1/public/reports/trending-content"


# --- NFT Operations Endpoints ---
print_header "Testing NFT Operations Endpoints"

# POST /api/v1/mint-memorial-entry-nft
MEMORIAL_ENTRY_PAYLOAD="{\"memorial_id\":\"test-memorial-$(date +%s)\",\"recipient_name\":\"Test Recipient\",\"sender_name\":\"Test Sender\",\"message\":\"This is a test memorial entry from the automated script.\",\"image_url\":\"https://placehold.co/600x400/000000/FFFFFF?text=TestMemorial\",\"xrp_ledger_wallet_address\":\"rPT1Sjq2YgrbJQdnPaQd84M22T9Jz7X2iG\"}"
MINT_RESPONSE=$(make_authenticated_post_request "/api/v1/mint-memorial-entry-nft" "$ACCESS_TOKEN" "$MEMORIAL_ENTRY_PAYLOAD")
if [ $? -eq 0 ]; then
    MINTED_NFT_TOKEN_ID=$(echo "$MINT_RESPONSE" | grep -o '"token_id":"[^"]*"' | head -1 | cut -d':' -f2 | tr -d '"')
    echo -e "${BLUE}Minted NFT Token ID obtained: $MINTED_NFT_TOKEN_ID${NC}"

    # GET /api/v1/nfts/my-nfts
    make_authenticated_get_request "/api/v1/nfts/my-nfts" "$ACCESS_TOKEN"

    # GET /api/v1/nfts/{nft_token_id}
    if [ -n "$MINTED_NFT_TOKEN_ID" ]; then
        make_authenticated_get_request "/api/v1/nfts/$MINTED_NFT_TOKEN_ID" "$ACCESS_TOKEN"
    else
        echo -e "${RED}ERROR: Could not extract Minted NFT Token ID for /api/v1/nfts/{nft_token_id} test.${NC}"
    fi
else
    echo -e "${RED}ERROR: Failed to mint memorial entry NFT. Subsequent NFT tests may fail.${NC}"
fi


# --- User Reports Endpoints ---
print_header "Testing User Reports Endpoints"
make_authenticated_get_request "/api/v1/user_reports/my-profile-summary" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/user_reports/my-nft-collection" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/user_reports/my-content" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/user_reports/my-activity-log" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/user_reports/my-earnings" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/user_reports/my-full-profile" "$ACCESS_TOKEN"


# --- Affiliate Reports Endpoints ---
print_header "Testing Affiliate Reports Endpoints"
make_authenticated_get_request "/api/v1/affiliate_reports/my-summary" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/affiliate_reports/my-referrals" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/affiliate_reports/my-clicks" "$ACCESS_TOKEN"
make_authenticated_get_request "/api/v1/affiliate_reports/my-earnings" "$ACCESS_TOKEN"


echo -e "\n${YELLOW}--- All tests completed ---${NC}"
