from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import routes at the bottom to avoid circular imports
# These imports are placed here intentionally
from crm_app.api import customers, deals