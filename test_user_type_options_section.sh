#!/bin/bash

# Script to test the User Type Options endpoints in the FastAPI application.
# This includes creating, retrieving, updating, and deleting user type options.

echo -e "\n\033[33m--- Testing User Type Options Endpoints ---\033[0m"

# IMPORTANT: API_BASE_URL is set to your server's public IP address, using HTTPS.
# The -L flag is added to curl commands to follow redirects (e.g., HTTP to HTTPS).
# The -k flag is added to curl commands to allow insecure server connections (e.g., for IP-based HTTPS access).
API_BASE_URL="https://31.97.129.206"

# Add a delay to allow the FastAPI application to fully start
echo -e "\033[33mWaiting 5 seconds for the FastAPI application to fully start...\033[0m"
sleep 5

# --- Step 1: Attempting to log in as superuser to obtain token... ---
echo -e "\n\033[33m--- Step 1: Attempting to log in as superuser to obtain token... ---\033[0m"
LOGIN_RESPONSE=$(curl -s -L -k -X POST "${API_BASE_URL}/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=guzzy_superuser&password=superuserpassword")

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')
HTTP_STATUS=$(echo "$LOGIN_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}') # Adjusted to get status after potential redirects

echo "$LOGIN_RESPONSE"
echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" == "200" ] && [ -n "$ACCESS_TOKEN" ] && [ "$ACCESS_TOKEN" != "null" ]; then
  echo -e "\033[32mSUCCESS: Access token obtained.\033[0m"
else
  echo -e "\033[31mERROR: Failed to obtain access token. Cannot proceed with authenticated tests.\033[0m"
  exit 1
fi

echo -e "\n\033[33m--- User Type Options Endpoints Tests Started ---\033[0m"

# --- Step 2: Create a new User Type Option ---
echo -e "\n\033[33m--- Step 2: Creating a new User Type Option (POST /api/v1/user_types/) ---\033[0m"
CREATE_RESPONSE=$(curl -s -L -k -X POST "${API_BASE_URL}/api/v1/user_types/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "TestUserType",
    "description": "A user type created for testing purposes.",
    "is_active": true
  }')

CREATED_USER_TYPE_ID=$(echo "$CREATE_RESPONSE" | jq -r '.id')
HTTP_STATUS=$(echo "$CREATE_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}')

echo "$CREATE_RESPONSE"
echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" == "201" ] && [ -n "$CREATED_USER_TYPE_ID" ] && [ "$CREATED_USER_TYPE_ID" != "null" ]; then
  echo -e "\033[32mSUCCESS: User Type Option created with ID: $CREATED_USER_TYPE_ID\033[0m"
else
  echo -e "\033[31mERROR: Failed to create User Type Option.\033[0m"
  exit 1
fi

# --- Step 3: Get all User Type Options ---
echo -e "\n\033[33m--- Step 3: Getting all User Type Options (GET /api/v1/user_types/) ---\033[0m"
GET_ALL_RESPONSE=$(curl -s -L -k -X GET "${API_BASE_URL}/api/v1/user_types/" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_STATUS=$(echo "$GET_ALL_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}')

echo "$GET_ALL_RESPONSE"
echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" == "200" ]; then
  # Check if the created user type ID is in the list
  if echo "$GET_ALL_RESPONSE" | jq -e ".[] | select(.id == \"$CREATED_USER_TYPE_ID\")" > /dev/null; then
    echo -e "\033[32mSUCCESS: Retrieved all User Type Options. Created User Type found in list.\033[0m"
  else
    echo -e "\033[31mERROR: Created User Type not found in the list of all User Type Options.\033[0m"
  fi
else
  echo -e "\033[31mERROR: Failed to get all User Type Options.\033[0m"
fi

# --- Step 4: Get a specific User Type Option by ID ---
echo -e "\n\033[33m--- Step 4: Getting a specific User Type Option by ID (GET /api/v1/user_types/{id}) ---\033[0m"
GET_BY_ID_RESPONSE=$(curl -s -L -k -X GET "${API_BASE_URL}/api/v1/user_types/$CREATED_USER_TYPE_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_STATUS=$(echo "$GET_BY_ID_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}')

echo "$GET_BY_ID_RESPONSE"
echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" == "200" ] && echo "$GET_BY_ID_RESPONSE" | jq -e ".id == \"$CREATED_USER_TYPE_ID\"" > /dev/null; then
  echo -e "\033[32mSUCCESS: Retrieved User Type Option by ID.\033[0m"
else
  echo -e "\033[31mERROR: Failed to get User Type Option by ID.\033[0m"
fi

# --- Step 5: Update the User Type Option ---
echo -e "\n\033[33m--- Step 5: Updating the User Type Option (PUT /api/v1/user_types/{id}) ---\033[0m"
UPDATE_RESPONSE=$(curl -s -L -k -X PUT "${API_BASE_URL}/api/v1/user_types/$CREATED_USER_TYPE_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "UpdatedTestUserType",
    "description": "An updated description for testing purposes.",
    "is_active": false
  }')

HTTP_STATUS=$(echo "$UPDATE_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}')

echo "$UPDATE_RESPONSE"
echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" == "200" ] && echo "$UPDATE_RESPONSE" | jq -e ".name == \"UpdatedTestUserType\" and .is_active == false" > /dev/null; then
  echo -e "\033[32mSUCCESS: User Type Option updated successfully.\033[0m"
else
  echo -e "\033[31mERROR: Failed to update User Type Option.\033[0m"
fi

# --- Step 6: Delete the User Type Option ---
echo -e "\n\033[33m--- Step 6: Deleting the User Type Option (DELETE /api/v1/user_types/{id}) ---\033[0m"
DELETE_RESPONSE=$(curl -s -L -k -X DELETE "${API_BASE_URL}/api/v1/user_types/$CREATED_USER_TYPE_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_STATUS=$(echo "$DELETE_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}')

echo "$DELETE_RESPONSE" # Should be empty or simple success message
echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" == "204" ]; then
  echo -e "\033[32mSUCCESS: User Type Option deleted successfully.\033[0m"
else
  echo -e "\033[31mERROR: Failed to delete User Type Option.\033[0m"
  # Attempt to retrieve to see if it still exists
  echo -e "\033[33mAttempting to retrieve deleted User Type Option to confirm failure...\033[0m"
  GET_DELETED_RESPONSE=$(curl -s -L -k -X GET "${API_BASE_URL}/api/v1/user_types/$CREATED_USER_TYPE_ID" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
  HTTP_STATUS_DELETED=$(echo "$GET_DELETED_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}')
  echo "$GET_DELETED_RESPONSE"
  echo "HTTP Status (after delete attempt): $HTTP_STATUS_DELETED"
  if [ "$HTTP_STATUS_DELETED" == "404" ]; then
    echo -e "\033[32m(Confirmed) User Type Option is indeed gone (404 Not Found).\033[0m"
  else
    echo -e "\033[31m(Warning) User Type Option might not have been deleted correctly.\033[0m"
  fi
  exit 1 # Exit with error if deletion failed
fi

# --- Step 7: Verify deletion by attempting to get the deleted User Type Option ---
echo -e "\n\033[33m--- Step 7: Verifying deletion of User Type Option (GET /api/v1/user_types/{id}) ---\033[0m"
VERIFY_DELETE_RESPONSE=$(curl -s -L -k -X GET "${API_BASE_URL}/api/v1/user_types/$CREATED_USER_TYPE_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_STATUS=$(echo "$VERIFY_DELETE_RESPONSE" | tail -n 2 | head -n 1 | grep -oP 'HTTP/\d\.\d \K\d{3}')

echo "$VERIFY_DELETE_RESPONSE"
echo "HTTP Status: $HTTP_STATUS"

if [ "$HTTP_STATUS" == "404" ]; then
  echo -e "\033[32mSUCCESS: User Type Option confirmed deleted (received 404 Not Found).\033[0m"
else
  echo -e "\033[31mERROR: User Type Option was not deleted successfully (expected 404, got $HTTP_STATUS).\033[0m"
  exit 1
fi

echo -e "\n\033[33m--- User Type Options Endpoints Tests Completed ---\033[0m"
