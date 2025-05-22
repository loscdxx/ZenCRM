from flask import jsonify, request, abort
from flask_login import login_required, current_user
from crm_app import db
from crm_app.api import api_bp
from crm_app.models import Deal, Customer, Activity
from datetime import datetime

@api_bp.route('/deals', methods=['GET'])
@login_required
def get_deals():
    """Get all deals as JSON"""
    deals = Deal.query.all()
    
    # Convert deals to JSON-serializable format
    deals_data = []
    for deal in deals:
        deals_data.append({
            'id': deal.id,
            'name': deal.name,
            'value': float(deal.value),
            'stage': deal.stage,
            'probability': deal.probability,
            'close_date': deal.close_date.isoformat() if deal.close_date else None,
            'description': deal.description,
            'customer_id': deal.customer_id,
            'customer_name': Customer.query.get(deal.customer_id).name if deal.customer_id else None,
            'created_at': deal.created_at.isoformat() if deal.created_at else None,
            'updated_at': deal.updated_at.isoformat() if deal.updated_at else None
        })
    
    return jsonify({'deals': deals_data})

@api_bp.route('/deals/<int:id>', methods=['GET'])
@login_required
def get_deal(id):
    """Get a specific deal as JSON"""
    deal = Deal.query.get_or_404(id)
    
    # Get related activities
    activities = Activity.query.filter_by(deal_id=id).all()
    activities_data = []
    
    for activity in activities:
        activities_data.append({
            'id': activity.id,
            'type': activity.type,
            'description': activity.description,
            'created_at': activity.created_at.isoformat() if activity.created_at else None
        })
    
    # Get customer info
    customer = Customer.query.get(deal.customer_id) if deal.customer_id else None
    customer_data = None
    if customer:
        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'company': customer.company
        }
    
    # Create deal data dictionary
    deal_data = {
        'id': deal.id,
        'name': deal.name,
        'value': float(deal.value),
        'stage': deal.stage,
        'probability': deal.probability,
        'close_date': deal.close_date.isoformat() if deal.close_date else None,
        'description': deal.description,
        'customer': customer_data,
        'activities': activities_data,
        'created_at': deal.created_at.isoformat() if deal.created_at else None,
        'updated_at': deal.updated_at.isoformat() if deal.updated_at else None
    }
    
    return jsonify({'deal': deal_data})

@api_bp.route('/deals', methods=['POST'])
@login_required
def create_deal():
    """Create a new deal"""
    # Check if request has JSON data
    if not request.json:
        abort(400, description="Request must be JSON")
    
    # Validate required fields
    required_fields = ['name', 'value', 'stage', 'customer_id']
    for field in required_fields:
        if field not in request.json:
            abort(400, description=f"Missing required field: {field}")
    
    # Validate customer exists
    customer_id = request.json.get('customer_id')
    customer = Customer.query.get(customer_id)
    if not customer:
        abort(404, description=f"Customer with ID {customer_id} not found")
    
    # Parse close_date if provided
    close_date = None
    if 'close_date' in request.json and request.json['close_date']:
        try:
            close_date = datetime.fromisoformat(request.json['close_date'])
        except ValueError:
            abort(400, description="Invalid close_date format. Use ISO format (YYYY-MM-DD)")
    
    # Create new deal
    deal = Deal(
        name=request.json.get('name'),
        value=request.json.get('value'),
        stage=request.json.get('stage'),
        probability=request.json.get('probability', 0),
        close_date=close_date,
        description=request.json.get('description', ''),
        customer_id=customer_id
    )
    
    db.session.add(deal)
    
    # Create activity for deal creation
    activity = Activity(
        type='Created',
        description='Deal created',
        deal_id=deal.id
    )
    db.session.add(activity)
    
    db.session.commit()
    
    # Return the created deal
    return jsonify({
        'deal': {
            'id': deal.id,
            'name': deal.name,
            'value': float(deal.value),
            'stage': deal.stage,
            'probability': deal.probability,
            'close_date': deal.close_date.isoformat() if deal.close_date else None,
            'description': deal.description,
            'customer_id': deal.customer_id,
            'created_at': deal.created_at.isoformat() if deal.created_at else None
        },
        'message': 'Deal created successfully'
    }), 201

@api_bp.route('/deals/<int:id>', methods=['PUT'])
@login_required
def update_deal(id):
    """Update a deal"""
    deal = Deal.query.get_or_404(id)
    
    # Check if request has JSON data
    if not request.json:
        abort(400, description="Request must be JSON")
    
    # Update deal fields if provided
    if 'name' in request.json:
        deal.name = request.json['name']
    if 'value' in request.json:
        deal.value = request.json['value']
    if 'stage' in request.json:
        old_stage = deal.stage
        new_stage = request.json['stage']
        deal.stage = new_stage
        
        # Create activity for stage change
        if old_stage != new_stage:
            activity = Activity(
                type='Stage Change',
                description=f'Deal stage changed from {old_stage} to {new_stage}',
                deal_id=deal.id
            )
            db.session.add(activity)
            
    if 'probability' in request.json:
        deal.probability = request.json['probability']
    if 'description' in request.json:
        deal.description = request.json['description']
    if 'customer_id' in request.json:
        # Validate customer exists
        customer_id = request.json['customer_id']
        customer = Customer.query.get(customer_id)
        if not customer:
            abort(404, description=f"Customer with ID {customer_id} not found")
        deal.customer_id = customer_id
    
    # Parse close_date if provided
    if 'close_date' in request.json:
        if request.json['close_date']:
            try:
                deal.close_date = datetime.fromisoformat(request.json['close_date'])
            except ValueError:
                abort(400, description="Invalid close_date format. Use ISO format (YYYY-MM-DD)")
        else:
            deal.close_date = None
    
    db.session.commit()
    
    return jsonify({
        'deal': {
            'id': deal.id,
            'name': deal.name,
            'value': float(deal.value),
            'stage': deal.stage,
            'probability': deal.probability,
            'close_date': deal.close_date.isoformat() if deal.close_date else None,
            'description': deal.description,
            'customer_id': deal.customer_id,
            'updated_at': deal.updated_at.isoformat() if deal.updated_at else None
        },
        'message': 'Deal updated successfully'
    })

@api_bp.route('/deals/<int:id>', methods=['DELETE'])
@login_required
def delete_deal(id):
    """Delete a deal"""
    deal = Deal.query.get_or_404(id)
    
    # Delete related activities
    Activity.query.filter_by(deal_id=id).delete()
    
    db.session.delete(deal)
    db.session.commit()
    
    return jsonify({
        'message': 'Deal deleted successfully'
    })