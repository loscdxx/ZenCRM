import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(test_config=None):
    """Create and configure the Flask application"""
    # Set the template and static folder paths explicitly
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir,
                instance_relative_config=True)

    # Configure the app
    if test_config is None:
        # Load the config from config.py
        app.config.from_object('crm_app.config.DevelopmentConfig')
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from crm_app.main import main_bp
    from crm_app.auth import auth_bp
    from crm_app.customers import customers_bp
    from crm_app.deals import deals_bp
    from crm_app.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(deals_bp)
    app.register_blueprint(api_bp)

    # Register error handlers
    from crm_app.errors import register_error_handlers
    register_error_handlers(app)

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Database tables created successfully')
        except Exception as e:
            app.logger.error(f'Error creating database tables: {str(e)}')

    return app