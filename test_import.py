"""
Test script to verify imports are working correctly.
Run this from the project root directory.
"""

try:
    from crm_app import create_app, db
    print("✅ Successfully imported crm_app module")
    
    app = create_app()
    print("✅ Successfully created app instance")
    
    with app.app_context():
        from crm_app.models import Customer
        customers = Customer.query.all()
        print(f"✅ Successfully queried database. Found {len(customers)} customers.")
        
        # Test API blueprint
        print("Testing API blueprint registration...")
        for rule in app.url_map.iter_rules():
            if 'api' in rule.endpoint:
                print(f"  ✅ Found API route: {rule}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()