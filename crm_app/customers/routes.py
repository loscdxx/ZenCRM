from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from crm_app import db
from crm_app.customers import customers_bp
from crm_app.models import Customer, Deal
from crm_app.forms import CustomerForm

@customers_bp.route('/')
@login_required
def list():
    """List all customers"""
    customers = Customer.query.all()
    return render_template('customers/list.html', customers=customers)

@customers_bp.route('/modern')
@login_required
def modern_list():
    """Modern UI for listing customers using API"""
    return render_template('customers/modern_list.html')

@customers_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new customer"""
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            address=form.address.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer created successfully!', 'success')
        return redirect(url_for('customers.view', id=customer.id))
    
    return render_template('customers/create.html', form=form, title='Create Customer')

@customers_bp.route('/<int:id>')
@login_required
def view(id):
    """View a specific customer"""
    customer = Customer.query.get_or_404(id)
    deals_query = Deal.query.filter_by(customer_id=id).all()

    # Format deal values and dates as strings
    deals = []
    for deal in deals_query:
        deal_dict = deal.__dict__.copy()
        deal_dict['value'] = f"{deal.value:,.0f}"
        deal_dict['probability'] = f"{deal.probability}"
        deal_dict['close_date'] = deal.close_date.strftime('%Y-%m-%d') if deal.close_date else ''
        deals.append(deal_dict)

    return render_template('customers/view.html', customer=customer, deals=deals)

@customers_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a customer"""
    customer = Customer.query.get_or_404(id)
    form = CustomerForm()
    
    if form.validate_on_submit():
        customer.name = form.name.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        customer.company = form.company.data
        customer.address = form.address.data
        customer.status = form.status.data
        customer.notes = form.notes.data
        
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers.view', id=customer.id))
    
    elif request.method == 'GET':
        form.name.data = customer.name
        form.email.data = customer.email
        form.phone.data = customer.phone
        form.company.data = customer.company
        form.address.data = customer.address
        form.status.data = customer.status
        form.notes.data = customer.notes
    
    return render_template('customers/edit.html', form=form, customer=customer, title='Edit Customer')

@customers_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a customer"""
    customer = Customer.query.get_or_404(id)
    
    # Check if customer has deals
    deals = Deal.query.filter_by(customer_id=id).all()
    if deals:
        flash('Cannot delete customer with active deals. Please delete or reassign deals first.', 'danger')
        return redirect(url_for('customers.view', id=id))
    
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customers.list'))