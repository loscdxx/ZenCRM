from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from crm_app.auth import routes