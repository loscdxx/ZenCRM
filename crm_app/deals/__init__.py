from flask import Blueprint

deals_bp = Blueprint('deals', __name__, url_prefix='/deals')

from crm_app.deals import routes