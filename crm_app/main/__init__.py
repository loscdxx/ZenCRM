from flask import Blueprint

main_bp = Blueprint('main', __name__)

from crm_app.main import routes