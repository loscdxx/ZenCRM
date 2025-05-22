from flask import jsonify, request, abort
from flask_login import login_required, current_user
from crm_app import db
from crm_app.api import api_bp
from crm_app.models import Customer, Deal

@api_bp.route('/customers', methods=['GET'])
@login_required
def get_customers():
    """Get all customers as JSON"""
    customers = Customer.query.all()
    
    # Convert customers to JSON-serializable format
    customers_data = []
    for customer in customers:
        customers_data.append({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'company': customer.company,
            'status': customer.status,
            'address': customer.address,
            'notes': customer.notes,
            'created_at': customer.created_at.isoformat() if customer.created_at else None,
            'updated_at': customer.updated_at.isoformat() if customer.updated_at else None
        })
    
    return jsonify({'customers': customers_data})

@api_bp.route('/customers/<int:id>', methods=['GET'])
@login_required
def get_customer(id):
    """Get a specific customer as JSON"""
    customer = Customer.query.get_or_404(id)
    
    # Get related deals
    deals = Deal.query.filter_by(customer_id=id).all()
    deals_data = []
    
    for deal in deals:
        deals_data.append({
            'id': deal.id,
            'name': deal.name,
            'value': float(deal.value),
            'stage': deal.stage,
            'probability': deal.probability,
            'close_date': deal.close_date.isoformat() if deal.close_date else None,
            'description': deal.description
        })
    
    # Create customer data dictionary
    customer_data = {
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'company': customer.company,
        'status': customer.status,
        'address': customer.address,
        'notes': customer.notes,
        'created_at': customer.created_at.isoformat() if customer.created_at else None,
        'updated_at': customer.updated_at.isoformat() if customer.updated_at else None,
        'deals': deals_data
    }
    
    return jsonify({'customer': customer_data})

@api_bp.route('/customers', methods=['POST'])
@login_required
def create_customer():
    """Create a new customer"""
    # Check if request has JSON data
    if not request.json:
        abort(400, description="Request must be JSON")
    
    # Validate required fields
    required_fields = ['name', 'email', 'company']
    for field in required_fields:
        if field not in request.json:
            abort(400, description=f"Missing required field: {field}")
    
    # Create new customer
    customer = Customer(
        name=request.json.get('name'),
        email=request.json.get('email'),
        phone=request.json.get('phone', ''),
        company=request.json.get('company'),
        address=request.json.get('address', ''),
        status=request.json.get('status', 'Pending'),
        notes=request.json.get('notes', '')
    )
    
    db.session.add(customer)
    db.session.commit()
    
    # Return the created customer
    return jsonify({
        'customer': {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'company': customer.company,
            'status': customer.status,
            'address': customer.address,
            'notes': customer.notes,
            'created_at': customer.created_at.isoformat() if customer.created_at else None
        },
        'message': 'Customer created successfully'
    }), 201

@api_bp.route('/customers/<int:id>', methods=['PUT'])
@login_required
def update_customer(id):
    """Update a customer"""
    customer = Customer.query.get_or_404(id)
    
    # Check if request has JSON data
    if not request.json:
        abort(400, description="Request must be JSON")
    
    # Update customer fields if provided
    if 'name' in request.json:
        customer.name = request.json['name']
    if 'email' in request.json:
        customer.email = request.json['email']
    if 'phone' in request.json:
        customer.phone = request.json['phone']
    if 'company' in request.json:
        customer.company = request.json['company']
    if 'address' in request.json:
        customer.address = request.json['address']
    if 'status' in request.json:
        customer.status = request.json['status']
    if 'notes' in request.json:
        customer.notes = request.json['notes']
    
    db.session.commit()
    
    return jsonify({
        'customer': {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'company': customer.company,
            'status': customer.status,
            'address': customer.address,
            'notes': customer.notes,
            'updated_at': customer.updated_at.isoformat() if customer.updated_at else None
        },
        'message': 'Customer updated successfully'
    })

@api_bp.route('/customers/<int:id>', methods=['DELETE'])
@login_required
def delete_customer(id):
    """Delete a customer"""
    customer = Customer.query.get_or_404(id)
    
    # Check if customer has deals
    deals = Deal.query.filter_by(customer_id=id).all()
    if deals:
        return jsonify({
            'error': 'Cannot delete customer with active deals',
            'message': 'Please delete or reassign deals first'
        }), 400
    
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({
        'message': 'Customer deleted successfully'
    })