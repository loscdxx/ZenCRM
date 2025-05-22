from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from models import db
from models.customer import Customer
from models.deal import Deal
from forms.deal import DealForm

deal_bp = Blueprint('deal', __name__, url_prefix='/deals')

@deal_bp.route('/')
@login_required
def list_deals():
    deals = Deal.query.filter_by(user_id=current_user.id).all()
    return render_template('deal/list.html', deals=deals)

@deal_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_deal():
    form = DealForm()
    
    # Get customers for the dropdown
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    form.customer_id.choices = [(c.id, f"{c.name} ({c.company or 'No Company'})") for c in customers]
    
    if form.validate_on_submit():
        # Verify customer belongs to user
        customer = Customer.query.filter_by(id=form.customer_id.data, user_id=current_user.id).first_or_404()
        
        deal = Deal(
            title=form.title.data,
            value=form.value.data,
            probability=form.probability.data,
            expected_close_date=form.expected_close_date.data,
            status=form.status.data,
            notes=form.notes.data,
            customer_id=form.customer_id.data,
            user_id=current_user.id
        )
        
        db.session.add(deal)
        db.session.commit()
        
        flash('Deal added successfully!', 'success')
        return redirect(url_for('deal.list_deals'))
    
    return render_template('deal/form.html', form=form, title='Add Deal')

@deal_bp.route('/<int:deal_id>')
@login_required
def view_deal(deal_id):
    deal = Deal.query.filter_by(id=deal_id, user_id=current_user.id).first_or_404()
    return render_template('deal/view.html', deal=deal)

@deal_bp.route('/<int:deal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_deal(deal_id):
    deal = Deal.query.filter_by(id=deal_id, user_id=current_user.id).first_or_404()
    form = DealForm(obj=deal)
    
    # Get customers for the dropdown
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    form.customer_id.choices = [(c.id, f"{c.name} ({c.company or 'No Company'})") for c in customers]
    
    if form.validate_on_submit():
        # Verify customer belongs to user
        customer = Customer.query.filter_by(id=form.customer_id.data, user_id=current_user.id).first_or_404()
        
        form.populate_obj(deal)
        db.session.commit()
        
        flash('Deal updated successfully!', 'success')
        return redirect(url_for('deal.view_deal', deal_id=deal.id))
    
    return render_template('deal/form.html', form=form, deal=deal, title='Edit Deal')

@deal_bp.route('/<int:deal_id>/delete', methods=['POST'])
@login_required
def delete_deal(deal_id):
    deal = Deal.query.filter_by(id=deal_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(deal)
    db.session.commit()
    
    flash('Deal deleted successfully!', 'success')
    return redirect(url_for('deal.list_deals'))

@deal_bp.route('/forecast')
@login_required
def forecast():
    # Get all open deals
    open_deals = Deal.query.filter_by(user_id=current_user.id, status='Open').all()
    
    # Calculate forecast by month
    forecast_by_month = {}
    for deal in open_deals:
        month_key = deal.expected_close_date.strftime('%Y-%m')
        if month_key not in forecast_by_month:
            forecast_by_month[month_key] = {
                'total': 0,
                'weighted': 0,
                'deals': []
            }
        
        forecast_by_month[month_key]['total'] += deal.value
        forecast_by_month[month_key]['weighted'] += deal.forecast_value
        forecast_by_month[month_key]['deals'].append(deal)
    
    # Sort by month
    sorted_forecast = dict(sorted(forecast_by_month.items()))
    
    return render_template('deal/forecast.html', forecast=sorted_forecast)