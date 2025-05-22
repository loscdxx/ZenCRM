import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from sqlalchemy import inspect

from crm_app import create_app, db
from app import init_db_command


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    # Create application context
    with app.app_context():
        yield app


class TestInitDbCommand:

    @patch('sqlalchemy.inspect')
    @patch('click.echo')
    @patch('crm_app.db.drop_all')
    @patch('crm_app.db.create_all')
    def test_init_db_command_success(self, mock_create_all, mock_drop_all, mock_echo, mock_inspect, app):
        """Test successful database initialization."""
        # Setup mock inspector
        mock_inspector = MagicMock()
        mock_inspect.return_value = mock_inspector

        # Mock inspector methods
        mock_inspector.get_table_names.return_value = ['users', 'customers', 'deals', 'activities']
        mock_inspector.get_columns.return_value = [
            {'name': 'id'},
            {'name': 'username'},
            {'name': 'email'},
            {'name': 'password_hash'},
            {'name': 'created_at'}
        ]

        # Call the command function directly
        with app.app_context():
            init_db_command()

        # Verify that the database operations were called
        mock_drop_all.assert_called_once()
        mock_create_all.assert_called_once()

        # Verify that the expected messages were echoed
        mock_echo.assert_any_call('Dropped all tables.')
        mock_echo.assert_any_call('Created all tables.')
        mock_echo.assert_any_call('Tables in database: users, customers, deals, activities')
        mock_echo.assert_any_call('Columns in users table: id, username, email, password_hash, created_at')
        mock_echo.assert_any_call('Database initialized successfully.')

    @patch('click.echo')
    @patch('crm_app.db.drop_all')
    def test_init_db_command_error(self, mock_drop_all, mock_echo, app):
        """Test database initialization with an error."""
        # Setup mock to raise an exception
        mock_drop_all.side_effect = Exception("Database error")

        # Call the command function and expect it to raise the exception
        with app.app_context():
            with pytest.raises(Exception) as excinfo:
                init_db_command()

            assert "Database error" in str(excinfo.value)

        # Verify that the error message was echoed
        mock_echo.assert_called_with('Error initializing database: Database error')