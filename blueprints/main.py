from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.customer import Customer
from models.deal import Deal

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get counts
    customer_count = Customer.query.filter_by(user_id=current_user.id).count()
    open_deals_count = Deal.query.filter_by(user_id=current_user.id, status='Open').count()
    won_deals_count = Deal.query.filter_by(user_id=current_user.id, status='Won').count()

    # Get total value of open deals
    open_deals = Deal.query.filter_by(user_id=current_user.id, status='Open').all()
    total_open_value = sum(deal.value for deal in open_deals)
    total_forecast_value = sum(deal.forecast_value for deal in open_deals)

    # Get recent customers and deals
    recent_customers = Customer.query.filter_by(user_id=current_user.id).order_by(Customer.created_at.desc()).limit(5).all()
    recent_deals = Deal.query.filter_by(user_id=current_user.id).order_by(Deal.created_at.desc()).limit(5).all()

    return render_template('dashboard.html',
                          customer_count=customer_count,
                          open_deals_count=open_deals_count,
                          won_deals_count=won_deals_count,
                          total_open_value=total_open_value,
                          total_forecast_value=total_forecast_value,
                          recent_customers=recent_customers,
                          recent_deals=recent_deals)

@main_bp.route('/contact')
def contact():
    """Contact us page"""
    return render_template('main/contact.html', title='Contact Us')

@main_bp.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('main/documentation.html', title='Documentation')

@main_bp.route('/api-reference')
def api_reference():
    """API Reference page"""
    return render_template('main/api_reference.html', title='API Reference')

@main_bp.route('/blog')
def blog():
    """Blog page"""
    return render_template('main/blog.html', title='Blog')

@main_bp.route('/community')
def community():
    """Community page"""
    return render_template('main/community.html', title='Community')

@main_bp.route('/about')
def about():
    """About Us page"""
    return render_template('main/about.html', title='About Us')

@main_bp.route('/careers')
def careers():
    """Careers page"""
    return render_template('main/careers.html', title='Careers')

@main_bp.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('main/privacy.html', title='Privacy Policy')

@main_bp.route('/terms')
def terms():
    """Terms and Conditions page"""
    return render_template('main/terms.html', title='Terms and Conditions')

@main_bp.route('/analytics')
def analytics():
    """Analytics page"""
    return render_template('main/analytics.html', title='Analytics')

@main_bp.route('/tasks')
def tasks():
    """Task Management page"""
    return render_template('main/tasks.html', title='Task Management')