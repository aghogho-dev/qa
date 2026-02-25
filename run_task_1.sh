#!/bin/bash

# Stop the script if any command fails
set -e

echo "Starting LendSQR SignUp, Login, and Create App Pipeline..."

# 1. Run Signup
echo "Step 1: Running Signup..."
pytest --headed tests/task_1/test_signup.py 

# Wait 30 seconds for the signup email
echo "Waiting 30 seconds for validation email delivery..."
sleep 30

# 2. Run Validation
echo "Step 2: Running Account Validation..."
pytest --headed tests/task_1/test_validate_account.py 

echo "Waiting 30 seconds after account activation..."
sleep 30

# 3. Run Login and App Creation and Get App ID and API Key
echo "Step 3: Creating App with Scopes..."
echo "Create App with Scopes: Create Customer, Activate Customer, Get Customers, Get Single Customer, Direct Debit, Direct Debit List Banks, Direct Debit Account Lookup, Bvn Initialize, Bvn Complete, CRC, Firstcentral, Oraculi Scoring" 
pytest --headed --scopes "Create Customer, Activate Customer, Get Customers, Get Single Customer, Direct Debit, Direct Debit List Banks, Direct Debit Account Lookup, Bvn Initialize, Bvn Complete, CRC, Firstcentral, Oraculi Scoring" tests/task_1/test_login.py

echo "--- Completed ---"
echo "API Key and App ID are in the .env_api file"
