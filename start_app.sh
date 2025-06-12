#!/bin/bash

# Explicitly set the PYTHONPATH to include your application's root directory
export PYTHONPATH="/var/www/guzzyandbash_app:$PYTHONPATH"

# Execute Uvicorn directly from the virtual environment's bin directory
# No 'exec' needed; Supervisor will manage this process directly
/var/www/guzzyandbash_app/venv/bin/uvicorn app.main:app --workers 2 --uds /var/www/guzzyandbash_app/run/uvicorn.sock --log-level info
