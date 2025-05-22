#!/usr/bin/env python3
"""
Test script to check if routes are working correctly.
"""

import os
import sys
from flask import url_for
from app import app

def test_routes():
    """Test if routes are working correctly."""
    with app.test_request_context():
        # Test main routes
        print("Testing main routes:")
        routes = [
            ('main.index', {}),
            ('main.dashboard', {}),
            ('main.documentation', {}),
            ('main.api_reference', {}),
            ('main.blog', {}),
            ('main.community', {}),
            ('main.about', {}),
            ('main.contact', {}),
        ]
        
        for route, kwargs in routes:
            try:
                url = url_for(route, **kwargs)
                print(f"✅ {route} -> {url}")
            except Exception as e:
                print(f"❌ {route} -> {str(e)}")
        
        # Test customer routes
        print("\nTesting customer routes:")
        routes = [
            ('customer.list_customers', {}),
        ]
        
        for route, kwargs in routes:
            try:
                url = url_for(route, **kwargs)
                print(f"✅ {route} -> {url}")
            except Exception as e:
                print(f"❌ {route} -> {str(e)}")
        
        # Test deal routes
        print("\nTesting deal routes:")
        routes = [
            ('deal.list_deals', {}),
        ]
        
        for route, kwargs in routes:
            try:
                url = url_for(route, **kwargs)
                print(f"✅ {route} -> {url}")
            except Exception as e:
                print(f"❌ {route} -> {str(e)}")

if __name__ == "__main__":
    test_routes()