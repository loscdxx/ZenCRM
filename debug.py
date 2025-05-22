"""
Debug script to identify issues with the Flask application.
"""
import os
import sys

print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))

try:
    print("\nTrying to import Flask...")
    from flask import Flask
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Error importing Flask: {str(e)}")

try:
    print("\nTrying to import crm_app...")
    from crm_app import create_app
    print("✅ crm_app imported successfully")
except Exception as e:
    print(f"❌ Error importing crm_app: {str(e)}")

try:
    print("\nTrying to create app...")
    from crm_app import create_app
    app = create_app()
    print("✅ App created successfully")
    
    print("\nRegistered blueprints:")
    for blueprint_name in app.blueprints:
        print(f"- {blueprint_name}")
    
    print("\nURL map:")
    for rule in app.url_map.iter_rules():
        print(f"- {rule.endpoint}: {rule.rule}")
except Exception as e:
    print(f"❌ Error creating app: {str(e)}")
    import traceback
    traceback.print_exc()

print("\nDebug complete.")