from datetime import datetime
from . import db

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    probability = db.Column(db.Integer, default=50)  # Percentage
    expected_close_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Open')  # Open, Won, Lost
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def forecast_value(self):
        return self.value * (self.probability / 100)