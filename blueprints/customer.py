from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.customer import Customer
from forms.customer import CustomerForm

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
@login_required
def list_customers():
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    return render_template('customer/list.html', customers=customers)

@customer_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    
    if form.validate_on_submit():
        customer = Customer(
            name=form.name.data,
            company=form.company.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        
        db.session.add(customer)
        db.session.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customer.list_customers'))
    
    return render_template('customer/form.html', form=form, title='Add Customer')

@customer_bp.route('/<int:customer_id>')
@login_required
def view_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first_or_404()
    return render_template('customer/view.html', customer=customer)

@customer_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first_or_404()
    form = CustomerForm(obj=customer)
    
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customer.view_customer', customer_id=customer.id))
    
    return render_template('customer/form.html', form=form, customer=customer, title='Edit Customer')

@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(customer)
    db.session.commit()
    
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customer.list_customers'))