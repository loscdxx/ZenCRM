from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from crm_app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User model for authentication and user management"""
    __tablename__ = 'users'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Customer(db.Model):
    """Customer model for storing customer information"""
    __tablename__ = 'customers'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    address = db.Column(db.String(200))
    status = db.Column(db.String(20), default='New')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    deals = db.relationship('Deal', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'

class Deal(db.Model):
    """Deal model for storing deal information"""
    __tablename__ = 'deals'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float)
    stage = db.Column(db.String(50), default='Qualification')
    probability = db.Column(db.Integer, default=0)  # Stored as percentage (0-100)
    close_date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # Relationships
    activities = db.relationship('Activity', backref='deal', lazy=True)

    def __repr__(self):
        return f'<Deal {self.name}>'

class Activity(db.Model):
    """Activity model for tracking deal activities"""
    __tablename__ = 'activities'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    deal_id = db.Column(db.Integer, db.ForeignKey('deals.id'), nullable=False)

    def __repr__(self):
        return f'<Activity {self.type} for Deal {self.deal_id}>'