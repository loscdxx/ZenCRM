#!/bin/bash
cd /Users/carlos.cabrera/Desktop
source new_venv/bin/activate

# Backup the original app.py
cp app.py app.py.backup

# Replace with the fixed version
cp app_fixed.py app.py

# Run the application
echo "Running the fixed application..."
python app.py