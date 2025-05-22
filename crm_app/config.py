import os
from pathlib import Path

# Get the absolute path to the instance folder
basedir = Path(__file__).parent.parent
instance_path = os.path.join(basedir, 'instance')

# Create instance directory if it doesn't exist
os.makedirs(instance_path, exist_ok=True)

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')

    # Use absolute path for SQLite database
    db_path = os.path.join(instance_path, 'crm.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{db_path}')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Log SQL queries for debugging

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # In production, ensure SECRET_KEY is set in environment variables
    # and use a proper database like PostgreSQL