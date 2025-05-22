#!/bin/bash
cd /Users/carlos.cabrera/Desktop/ZenCRM
source new_venv/bin/activate

# Add the current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/Users/carlos.cabrera/Desktop/ZenCRM

# Run the fix script first
python fix_app.py

# Run the application
echo -e "\n🚀 Starting the application...\n"
python app.py