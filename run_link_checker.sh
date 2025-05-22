#!/bin/bash

# Install required dependencies
pip install -r requirements-updated.txt

# Run the link checker
echo "Running link checker..."
python link_checker.py

# Ask if user wants to fix links
read -p "Do you want to fix broken links? (y/n): " fix_links

if [[ $fix_links == "y" || $fix_links == "Y" ]]; then
    echo "Fixing broken links..."
    python link_checker.py --fix
    
    echo "Restarting the application to apply changes..."
    # Kill any running Flask processes
    pkill -f "flask run" || true
    
    # Start the application in the background
    flask run --port=5002 &
    
    # Wait for the application to start
    sleep 2
    
    # Run the link checker again to verify fixes
    echo "Verifying fixes..."
    python link_checker.py
fi

echo "Link checker completed!"