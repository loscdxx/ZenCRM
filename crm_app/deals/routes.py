from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from crm_app import db
from crm_app.deals import deals_bp
from crm_app.models import Deal, Customer, Activity
from crm_app.forms import DealForm, ActivityForm
from datetime import datetime
from wtforms import SelectField
from wtforms.validators import DataRequired

@deals_bp.route('/')
@login_required
def list():
    """List all deals"""
    deals = Deal.query.all()
    deals_with_customers = []
    
    for deal in deals:
        customer = Customer.query.get(deal.customer_id)
        deals_with_customers.append({
            'id': deal.id,
            'name': deal.name,
            'customer_id': customer.id,
            'customer_name': customer.name,
            'value': f"{deal.value:,.0f}",
            'stage': deal.stage,
            'probability': f"{deal.probability}%",
            'close_date': deal.close_date.strftime('%Y-%m-%d') if deal.close_date else ''
        })
    
    return render_template('deals/list.html', deals=deals_with_customers)

@deals_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new deal"""
    form = DealForm()

    # Get customers for the customer selection dropdown
    customers = Customer.query.all()
    customer_choices = [(str(c.id), c.name) for c in customers]
    form.customer_id.choices = customer_choices

    if form.validate_on_submit():
        deal = Deal(
            name=form.name.data,
            value=form.value.data,
            stage=form.stage.data,
            probability=int(form.probability.data),
            close_date=form.close_date.data,
            description=form.description.data,
            customer_id=int(form.customer_id.data)
        )
        db.session.add(deal)
        db.session.commit()  # Commit first to get the deal.id

        # Add creation activity
        activity = Activity(
            type='Created',
            description=f'Deal created',
            deal_id=deal.id
        )
        db.session.add(activity)
        db.session.commit()  # Commit again for the activity

        flash('Deal created successfully!', 'success')
        return redirect(url_for('deals.view', id=deal.id))
    
    return render_template('deals/create.html', form=form, title='Create Deal')

@deals_bp.route('/<int:id>')
@login_required
def view(id):
    """View a specific deal"""
    deal = Deal.query.get_or_404(id)
    customer = Customer.query.get(deal.customer_id)
    activities = Activity.query.filter_by(deal_id=id).order_by(Activity.date.desc()).all()

    return render_template('deals/view.html', deal=deal, customer=customer, activities=activities)

@deals_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a deal"""
    deal = Deal.query.get_or_404(id)
    form = DealForm()

    # Get customers for the customer selection dropdown
    customers = Customer.query.all()
    customer_choices = [(str(c.id), c.name) for c in customers]
    form.customer_id.choices = customer_choices
    
    if form.validate_on_submit():
        old_stage = deal.stage
        
        deal.name = form.name.data
        deal.value = form.value.data
        deal.stage = form.stage.data
        deal.probability = int(form.probability.data)
        deal.close_date = form.close_date.data
        deal.description = form.description.data
        deal.customer_id = int(form.customer_id.data)
        
        # Add stage change activity if stage changed
        if old_stage != form.stage.data:
            activity = Activity(
                type='Stage Change',
                description=f'Deal stage changed from {old_stage} to {form.stage.data}',
                deal_id=deal.id
            )
            db.session.add(activity)
        
        db.session.commit()
        flash('Deal updated successfully!', 'success')
        return redirect(url_for('deals.view', id=deal.id))
    
    elif request.method == 'GET':
        form.name.data = deal.name
        form.value.data = deal.value
        form.stage.data = deal.stage
        form.probability.data = str(deal.probability)
        form.close_date.data = deal.close_date
        form.description.data = deal.description
        form.customer_id.data = str(deal.customer_id)
    
    return render_template('deals/edit.html', form=form, deal=deal, title='Edit Deal')

@deals_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a deal"""
    deal = Deal.query.get_or_404(id)
    
    # Delete associated activities
    Activity.query.filter_by(deal_id=id).delete()
    
    db.session.delete(deal)
    db.session.commit()
    flash('Deal deleted successfully!', 'success')
    return redirect(url_for('deals.list'))

@deals_bp.route('/<int:id>/activity', methods=['GET', 'POST'])
@login_required
def add_activity(id):
    """Add an activity to a deal"""
    deal = Deal.query.get_or_404(id)
    form = ActivityForm()

    if form.validate_on_submit():
        activity = Activity(
            type=form.type.data,
            description=form.description.data,
            date=form.date.data if form.date.data else datetime.now(),
            deal_id=deal.id
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity added successfully!', 'success')
        return redirect(url_for('deals.view', id=deal.id))

    return render_template('deals/activity.html', form=form, deal=deal)