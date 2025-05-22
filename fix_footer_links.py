#!/usr/bin/env python3
"""
Script to fix footer links in the ZenCRM application.
"""

import os
import sys
import re

def fix_footer_links():
    """Fix footer links in the base.html templates."""
    base_html_paths = [
        os.path.join('templates', 'base.html'),
        os.path.join('crm_app', 'templates', 'base.html')
    ]
    
    success = True
    
    for base_html_path in base_html_paths:
        if not os.path.exists(base_html_path):
            print(f"Error: {base_html_path} not found.")
            success = False
            continue
        
        with open(base_html_path, 'r') as f:
            content = f.read()
        
        # Fix Quick Links section
        content = re.sub(
            r'<div class="footer-section">\s*<h3 class="footer-title">Quick Links</h3>\s*<a href="\{\{ url_for\(\'.*?\'\) \}\}" class="footer-link">Home</a>\s*<a href="\{\{ url_for\(\'.*?\'\) \}\}" class="footer-link">Dashboard</a>\s*<a href="\{\{ url_for\(\'.*?\'\) \}\}" class="footer-link">Customers</a>\s*<a href="\{\{ url_for\(\'.*?\'\) \}\}" class="footer-link">Deals</a>\s*</div>',
            '''<div class="footer-section">
                    <h3 class="footer-title">Quick Links</h3>
                    <a href="{{ url_for('main.index') }}" class="footer-link">Home</a>
                    <a href="{{ url_for('main.dashboard') }}" class="footer-link">Dashboard</a>
                    <a href="{{ url_for('customer.list_customers') }}" class="footer-link">Customers</a>
                    <a href="{{ url_for('deal.list_deals') }}" class="footer-link">Deals</a>
                </div>''',
            content
        )
        
        # Add Resources section if it doesn't exist
        if '<h3 class="footer-title">Resources</h3>' not in content:
            content = re.sub(
                r'(<div class="footer-section">\s*<h3 class="footer-title">Quick Links</h3>.*?</div>)',
                r'\1\n                <div class="footer-section">\n                    <h3 class="footer-title">Resources</h3>\n                    <a href="{{ url_for(\'main.documentation\') }}" class="footer-link">Documentation</a>\n                    <a href="{{ url_for(\'main.api_reference\') }}" class="footer-link">API Reference</a>\n                    <a href="{{ url_for(\'main.blog\') }}" class="footer-link">Blog</a>\n                    <a href="{{ url_for(\'main.community\') }}" class="footer-link">Community</a>\n                </div>',
                content,
                flags=re.DOTALL
            )
        else:
            # Fix Resources section
            content = re.sub(
                r'<div class="footer-section">\s*<h3 class="footer-title">Resources</h3>.*?</div>',
                '''<div class="footer-section">
                    <h3 class="footer-title">Resources</h3>
                    <a href="{{ url_for('main.documentation') }}" class="footer-link">Documentation</a>
                    <a href="{{ url_for('main.api_reference') }}" class="footer-link">API Reference</a>
                    <a href="{{ url_for('main.blog') }}" class="footer-link">Blog</a>
                    <a href="{{ url_for('main.community') }}" class="footer-link">Community</a>
                </div>''',
                content,
                flags=re.DOTALL
            )
        
        # Add Company section if it doesn't exist
        if '<h3 class="footer-title">Company</h3>' not in content:
            content = re.sub(
                r'(<div class="footer-section">\s*<h3 class="footer-title">Contact</h3>.*?</div>)',
                r'\1\n                <div class="footer-section">\n                    <h3 class="footer-title">Company</h3>\n                    <a href="{{ url_for(\'main.about\') }}" class="footer-link">About Us</a>\n                    <a href="{{ url_for(\'main.careers\') }}" class="footer-link">Careers</a>\n                    <a href="{{ url_for(\'main.privacy\') }}" class="footer-link">Privacy Policy</a>\n                    <a href="{{ url_for(\'main.terms\') }}" class="footer-link">Terms & Conditions</a>\n                </div>',
                content,
                flags=re.DOTALL
            )
        else:
            # Fix Company section
            content = re.sub(
                r'<div class="footer-section">\s*<h3 class="footer-title">Company</h3>.*?</div>',
                '''<div class="footer-section">
                    <h3 class="footer-title">Company</h3>
                    <a href="{{ url_for('main.about') }}" class="footer-link">About Us</a>
                    <a href="{{ url_for('main.careers') }}" class="footer-link">Careers</a>
                    <a href="{{ url_for('main.privacy') }}" class="footer-link">Privacy Policy</a>
                    <a href="{{ url_for('main.terms') }}" class="footer-link">Terms & Conditions</a>
                </div>''',
                content,
                flags=re.DOTALL
            )
        
        with open(base_html_path, 'w') as f:
            f.write(content)
        
        print(f"Fixed footer links in {base_html_path}.")
    
    return success

if __name__ == "__main__":
    fix_footer_links()