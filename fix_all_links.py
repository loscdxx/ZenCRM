#!/usr/bin/env python3
"""
Script to fix all links in the ZenCRM application.
This script fixes both navigation and footer links in the base.html template
and ensures all routes are properly defined in the blueprints.
"""

import os
import re
import sys

def fix_base_template():
    """Fix links in the base.html template."""
    base_html_path = os.path.join('templates', 'base.html')
    
    if not os.path.exists(base_html_path):
        print(f"Error: {base_html_path} not found.")
        return False
    
    with open(base_html_path, 'r') as f:
        content = f.read()
    
    # Fix navigation links
    content = re.sub(
        r'<a href="\{\{ url_for\(\'index\'\) \}\}" class="navbar-brand">',
        '<a href="{{ url_for(\'main.index\') }}" class="navbar-brand">',
        content
    )
    
    content = re.sub(
        r'<a href="\{\{ url_for\(\'dashboard\'\) \}\}" class="nav-link">',
        '<a href="{{ url_for(\'main.dashboard\') }}" class="nav-link">',
        content
    )
    
    content = re.sub(
        r'<a href="\{\{ url_for\(\'customers_list\'\) \}\}" class="nav-link">',
        '<a href="{{ url_for(\'customers.list\') }}" class="nav-link">',
        content
    )
    
    content = re.sub(
        r'<a href="\{\{ url_for\(\'deals_list\'\) \}\}" class="nav-link">',
        '<a href="{{ url_for(\'deals.list\') }}" class="nav-link">',
        content
    )
    
    content = re.sub(
        r'<a href="\{\{ url_for\(\'login\'\) \}\}" class="nav-link">',
        '<a href="{{ url_for(\'auth.login\') }}" class="nav-link">',
        content
    )
    
    content = re.sub(
        r'<a href="\{\{ url_for\(\'register\'\) \}\}" class="nav-link">',
        '<a href="{{ url_for(\'auth.register\') }}" class="nav-link">',
        content
    )
    
    content = re.sub(
        r'<a href="\{\{ url_for\(\'logout\'\) \}\}" class="nav-link">',
        '<a href="{{ url_for(\'auth.logout\') }}" class="nav-link">',
        content
    )
    
    # Fix footer links - Quick Links section
    content = re.sub(
        r'<div class="footer-section">\s*<h3 class="footer-title">Quick Links</h3>\s*<a href="\{\{ url_for\(\'main.index\'\) \}\}" class="footer-link">Home</a>\s*<a href="\{\{ url_for\(\'main.dashboard\'\) \}\}" class="footer-link">Dashboard</a>\s*<a href="\{\{ url_for\(\'customer.list_customers\'\) \}\}" class="footer-link">Customers</a>\s*<a href="\{\{ url_for\(\'deal.list_deals\'\) \}\}" class="footer-link">Deals</a>\s*</div>',
        '''<div class="footer-section">
                    <h3 class="footer-title">Quick Links</h3>
                    <a href="{{ url_for('main.index') }}" class="footer-link">Home</a>
                    <a href="{{ url_for('main.dashboard') }}" class="footer-link">Dashboard</a>
                    <a href="{{ url_for('customers.list') }}" class="footer-link">Customers</a>
                    <a href="{{ url_for('deals.list') }}" class="footer-link">Deals</a>
                </div>''',
        content
    )
    
    # Fix footer links - Resources section
    content = re.sub(
        r'<div class="footer-section">\s*<h3 class="footer-title">Resources</h3>\s*<a href="\{\{ url_for\(\'main.documentation\'\) \}\}" class="footer-link">Documentation</a>\s*<a href="\{\{ url_for\(\'main.api_reference\'\) \}\}" class="footer-link">API Reference</a>\s*<a href="\{\{ url_for\(\'main.blog\'\) \}\}" class="footer-link">Blog</a>\s*<a href="\{\{ url_for\(\'main.community\'\) \}\}" class="footer-link">Community</a>\s*</div>',
        '''<div class="footer-section">
                    <h3 class="footer-title">Resources</h3>
                    <a href="{{ url_for('main.documentation') }}" class="footer-link">Documentation</a>
                    <a href="{{ url_for('main.api_reference') }}" class="footer-link">API Reference</a>
                    <a href="{{ url_for('main.blog') }}" class="footer-link">Blog</a>
                    <a href="{{ url_for('main.community') }}" class="footer-link">Community</a>
                </div>''',
        content
    )
    
    with open(base_html_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed links in {base_html_path}.")
    return True

def ensure_main_routes():
    """Ensure all required routes are defined in the main blueprint."""
    main_routes_path = os.path.join('crm_app', 'main', 'routes.py')
    
    if not os.path.exists(main_routes_path):
        print(f"Error: {main_routes_path} not found.")
        return False
    
    with open(main_routes_path, 'r') as f:
        content = f.read()
    
    # Check if documentation route exists, if not add it
    if '@main_bp.route(\'/documentation\')' not in content:
        content = content.replace(
            '@main_bp.route(\'/about\')',
            '''@main_bp.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('about.html', title='Documentation')

@main_bp.route('/about')''',
            1
        )
    
    # Check if api_reference route exists, if not add it
    if '@main_bp.route(\'/api-reference\')' not in content and '@main_bp.route(\'/api_reference\')' not in content:
        content = content.replace(
            '@main_bp.route(\'/about\')',
            '''@main_bp.route('/api-reference')
def api_reference():
    """API Reference page"""
    return render_template('api_documentation.html', title='API Reference')

@main_bp.route('/about')''',
            1
        )
    
    # Check if blog route exists, if not add it
    if '@main_bp.route(\'/blog\')' not in content:
        content = content.replace(
            '@main_bp.route(\'/about\')',
            '''@main_bp.route('/blog')
def blog():
    """Blog page"""
    return render_template('about.html', title='Blog')

@main_bp.route('/about')''',
            1
        )
    
    # Check if community route exists, if not add it
    if '@main_bp.route(\'/community\')' not in content:
        content = content.replace(
            '@main_bp.route(\'/about\')',
            '''@main_bp.route('/community')
def community():
    """Community page"""
    return render_template('about.html', title='Community')

@main_bp.route('/about')''',
            1
        )
    
    with open(main_routes_path, 'w') as f:
        f.write(content)
    
    print(f"Ensured all required routes are defined in {main_routes_path}.")
    return True

def create_missing_templates():
    """Create any missing template files."""
    template_dir = os.path.join('crm_app', 'templates')
    
    # Ensure the main directory exists
    main_dir = os.path.join(template_dir, 'main')
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
        print(f"Created directory: {main_dir}")
    
    # Create documentation.html if it doesn't exist
    doc_path = os.path.join(main_dir, 'documentation.html')
    if not os.path.exists(doc_path):
        with open(doc_path, 'w') as f:
            f.write('''{% extends "base.html" %}

{% block title %}Documentation - ZenCRM{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Documentation</h1>
</div>

<div class="content-section">
    <h2>Getting Started</h2>
    <p>Welcome to the ZenCRM documentation. This guide will help you get started with our CRM system.</p>
    
    <h3>Installation</h3>
    <p>To install ZenCRM, follow these steps:</p>
    <ol>
        <li>Clone the repository</li>
        <li>Install dependencies with <code>pip install -r requirements.txt</code></li>
        <li>Initialize the database with <code>flask init-db</code></li>
        <li>Run the application with <code>flask run</code></li>
    </ol>
    
    <h3>Features</h3>
    <ul>
        <li>Customer management</li>
        <li>Deal tracking</li>
        <li>Activity logging</li>
        <li>Sales forecasting</li>
    </ul>
</div>
{% endblock %}''')
        print(f"Created template: {doc_path}")
    
    # Create api_reference.html if it doesn't exist
    api_path = os.path.join(main_dir, 'api_reference.html')
    if not os.path.exists(api_path):
        with open(api_path, 'w') as f:
            f.write('''{% extends "base.html" %}

{% block title %}API Reference - ZenCRM{% endblock %}

{% block content %}
<div class="page-header">
    <h1>API Reference</h1>
</div>

<div class="content-section">
    <h2>REST API</h2>
    <p>ZenCRM provides a RESTful API for integrating with other systems.</p>
    
    <h3>Authentication</h3>
    <p>All API requests require authentication using an API key.</p>
    <pre><code>curl -H "Authorization: Bearer YOUR_API_KEY" https://api.zencrm.com/v1/customers</code></pre>
    
    <h3>Endpoints</h3>
    <h4>Customers</h4>
    <ul>
        <li><code>GET /api/customers</code> - List all customers</li>
        <li><code>GET /api/customers/{id}</code> - Get a specific customer</li>
        <li><code>POST /api/customers</code> - Create a new customer</li>
        <li><code>PUT /api/customers/{id}</code> - Update a customer</li>
        <li><code>DELETE /api/customers/{id}</code> - Delete a customer</li>
    </ul>
    
    <h4>Deals</h4>
    <ul>
        <li><code>GET /api/deals</code> - List all deals</li>
        <li><code>GET /api/deals/{id}</code> - Get a specific deal</li>
        <li><code>POST /api/deals</code> - Create a new deal</li>
        <li><code>PUT /api/deals/{id}</code> - Update a deal</li>
        <li><code>DELETE /api/deals/{id}</code> - Delete a deal</li>
    </ul>
</div>
{% endblock %}''')
        print(f"Created template: {api_path}")
    
    # Create blog.html if it doesn't exist
    blog_path = os.path.join(main_dir, 'blog.html')
    if not os.path.exists(blog_path):
        with open(blog_path, 'w') as f:
            f.write('''{% extends "base.html" %}

{% block title %}Blog - ZenCRM{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Blog</h1>
</div>

<div class="content-section">
    <article class="blog-post">
        <h2>Maximizing Customer Relationships with ZenCRM</h2>
        <p class="blog-meta">Posted on May 15, 2023 by Admin</p>
        <p>Learn how to leverage ZenCRM features to build stronger customer relationships and increase sales.</p>
        <a href="#" class="btn btn-primary">Read More</a>
    </article>
    
    <article class="blog-post">
        <h2>5 Tips for Effective Sales Pipeline Management</h2>
        <p class="blog-meta">Posted on April 28, 2023 by Admin</p>
        <p>Discover best practices for managing your sales pipeline and closing more deals.</p>
        <a href="#" class="btn btn-primary">Read More</a>
    </article>
    
    <article class="blog-post">
        <h2>New Features: April 2023 Update</h2>
        <p class="blog-meta">Posted on April 10, 2023 by Admin</p>
        <p>Check out the latest features and improvements in our April 2023 update.</p>
        <a href="#" class="btn btn-primary">Read More</a>
    </article>
</div>
{% endblock %}''')
        print(f"Created template: {blog_path}")
    
    # Create community.html if it doesn't exist
    community_path = os.path.join(main_dir, 'community.html')
    if not os.path.exists(community_path):
        with open(community_path, 'w') as f:
            f.write('''{% extends "base.html" %}

{% block title %}Community - ZenCRM{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Community</h1>
</div>

<div class="content-section">
    <h2>Join Our Community</h2>
    <p>Connect with other ZenCRM users, share best practices, and get help from our community.</p>
    
    <div class="community-channels">
        <div class="channel-card">
            <h3>Forum</h3>
            <p>Ask questions, share ideas, and connect with other users on our forum.</p>
            <a href="#" class="btn btn-primary">Visit Forum</a>
        </div>
        
        <div class="channel-card">
            <h3>Slack</h3>
            <p>Join our Slack workspace for real-time discussions and networking.</p>
            <a href="#" class="btn btn-primary">Join Slack</a>
        </div>
        
        <div class="channel-card">
            <h3>GitHub</h3>
            <p>Contribute to ZenCRM development or report issues on GitHub.</p>
            <a href="#" class="btn btn-primary">GitHub Repo</a>
        </div>
    </div>
    
    <h2>Upcoming Events</h2>
    <div class="events-list">
        <div class="event-card">
            <h3>ZenCRM User Conference 2023</h3>
            <p>Date: September 15-17, 2023</p>
            <p>Location: San Francisco, CA</p>
            <a href="#" class="btn btn-secondary">Learn More</a>
        </div>
        
        <div class="event-card">
            <h3>Webinar: Advanced Deal Management</h3>
            <p>Date: June 5, 2023</p>
            <p>Time: 10:00 AM PST</p>
            <a href="#" class="btn btn-secondary">Register</a>
        </div>
    </div>
</div>
{% endblock %}''')
        print(f"Created template: {community_path}")
    
    return True

def main():
    """Main function to fix all links."""
    print("Starting to fix all links in the ZenCRM application...")
    
    # Fix base template
    if not fix_base_template():
        print("Failed to fix base template.")
        return False
    
    # Ensure all required routes are defined
    if not ensure_main_routes():
        print("Failed to ensure all required routes are defined.")
        return False
    
    # Create missing templates
    if not create_missing_templates():
        print("Failed to create missing templates.")
        return False
    
    print("\nAll links have been fixed successfully!")
    print("To verify, run the check_all_links.go program after starting the application.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)