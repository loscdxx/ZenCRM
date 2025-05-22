from flask import render_template, current_app, flash, redirect, url_for, request
from flask_login import login_required, current_user
from crm_app.main import main_bp
from crm_app.models import Customer, Deal, Activity
from crm_app.forms import ContactForm
from sqlalchemy import func
from datetime import datetime, timedelta

@main_bp.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@main_bp.route('/api-reference')
def api_reference():
    """API Reference page"""
    return render_template('api_reference.html')

@main_bp.route('/api-documentation')
def api_documentation():
    """API Documentation page (legacy route)"""
    return redirect(url_for('main.api_reference'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route with summary statistics and recent activities"""
    try:
        # Get real statistics from the database
        total_customers = Customer.query.count()
        active_deals = Deal.query.filter(Deal.stage != 'Closed Won', Deal.stage != 'Closed Lost').count()

        # Get deals closed this month
        first_day_of_month = datetime.today().replace(day=1)
        closed_deals_month = Deal.query.filter(
            Deal.stage == 'Closed Won',
            Deal.updated_at >= first_day_of_month
        ).count()

        # Calculate revenue for the month
        revenue_month = Deal.query.filter(
            Deal.stage == 'Closed Won',
            Deal.updated_at >= first_day_of_month
        ).with_entities(func.sum(Deal.value)).scalar() or 0

        stats = {
            'total_customers': total_customers,
            'active_deals': active_deals,
            'closed_deals_month': closed_deals_month,
            'revenue_month': f"{revenue_month:,.0f}"
        }

        # Get recent activities
        recent_activities = []
        activities = Activity.query.order_by(Activity.date.desc()).limit(5).all()

        for activity in activities:
            deal = Deal.query.get(activity.deal_id)
            customer = Customer.query.get(deal.customer_id)

            status_map = {
                'Qualification': 'info',
                'Proposal': 'primary',
                'Negotiation': 'warning',
                'Closing': 'warning',
                'Closed Won': 'success',
                'Closed Lost': 'danger'
            }

            recent_activities.append({
                'date': activity.date.strftime('%Y-%m-%d'),
                'description': activity.description,
                'customer_id': customer.id,
                'customer_name': customer.name,
                'deal_id': deal.id,
                'deal_name': deal.name,
                'status': deal.stage,
                'status_color': status_map.get(deal.stage, 'info')
            })

        # Get pipeline stages
        pipeline_data = {}
        stages = ['Qualification', 'Proposal', 'Negotiation', 'Closing']

        for stage in stages:
            deals = Deal.query.filter_by(stage=stage).all()
            stage_value = sum(deal.value for deal in deals)

            pipeline_deals = []
            for deal in deals[:2]:  # Limit to 2 deals per stage for display
                customer = Customer.query.get(deal.customer_id)
                pipeline_deals.append({
                    'id': deal.id,
                    'name': deal.name,
                    'customer_id': customer.id,
                    'customer_name': customer.name,
                    'value': f"{deal.value:,.0f}"
                })

            pipeline_data[stage] = {
                'name': stage,
                'count': len(deals),
                'value': f"{stage_value:,.0f}",
                'deals': pipeline_deals
            }

        pipeline_stages = list(pipeline_data.values())

        return render_template('dashboard.html',
                              stats=stats,
                              recent_activities=recent_activities,
                              pipeline_stages=pipeline_stages)
    except Exception as e:
        current_app.logger.error(f"Dashboard error: {str(e)}")
        flash(f"Error loading dashboard: {str(e)}. Please make sure you have initialized the database with 'flask init-db'.", 'danger')
        return render_template('dashboard.html',
                              stats={'total_customers': 0, 'active_deals': 0, 'closed_deals_month': 0, 'revenue_month': '0'},
                              recent_activities=[],
                              pipeline_stages=[])

@main_bp.route('/time-savings')
def time_savings():
    """Devs Time Savings Calculator page"""
    return render_template('time_savings.html')

@main_bp.route('/about')
def about():
    """About Us page"""
    return render_template('about.html')

@main_bp.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html', title='Documentation')

@main_bp.route('/blog')
def blog():
    """Blog page"""
    return render_template('blog.html', title='Blog')

@main_bp.route('/community')
def community():
    """Community page"""
    return render_template('community.html', title='Community')

@main_bp.route('/careers')
def careers():
    """Careers page"""
    return render_template('careers.html', title='Careers')

@main_bp.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html', title='Privacy Policy')

@main_bp.route('/terms')
def terms():
    """Terms and Conditions page"""
    return render_template('terms.html', title='Terms and Conditions')

@main_bp.route('/analytics')
@login_required
def analytics():
    """Analytics page"""
    return render_template('analytics.html', title='Analytics')

@main_bp.route('/tasks')
@login_required
def tasks():
    """Task Management page"""
    return render_template('tasks.html', title='Task Management')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact us page with form"""
    form = ContactForm()

    if form.validate_on_submit():
        # In a real application, you would save this to a database or send an email
        # For now, we'll just show a success message
        flash(f'Thank you, {form.name.data}! Your message has been sent. We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))

    return render_template('contact.html', form=form, title='Contact Us')