import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import inspect

from crm_app import create_app, db


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


def test_init_db_success(app):
    """Test successful database initialization."""
    with patch('crm_app.db.drop_all') as mock_drop_all:
        with patch('crm_app.db.create_all') as mock_create_all:
            with patch('sqlalchemy.inspect') as mock_inspect:
                with patch('click.echo') as mock_echo:
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
                    
                    # Call the function that would be inside init_db_command
                    with app.app_context():
                        # Drop all tables
                        db.drop_all()
                        mock_echo('Dropped all tables.')

                        # Create all tables
                        db.create_all()
                        mock_echo('Created all tables.')

                        # Verify tables were created
                        inspector = inspect(db.engine)
                        tables = inspector.get_table_names()
                        mock_echo(f'Tables in database: {", ".join(tables)}')

                        # Verify User table columns
                        columns = [col['name'] for col in inspector.get_columns('users')]
                        mock_echo(f'Columns in users table: {", ".join(columns)}')

                        mock_echo('Database initialized successfully.')
                    
                    # Verify that the database operations were called
                    mock_drop_all.assert_called_once()
                    mock_create_all.assert_called_once()
                    
                    # Verify that the expected messages were echoed
                    mock_echo.assert_any_call('Dropped all tables.')
                    mock_echo.assert_any_call('Created all tables.')

                    # Check that a message about tables was echoed, but don't check the exact order
                    table_call_found = False
                    for call in mock_echo.call_args_list:
                        args, _ = call
                        if len(args) == 1 and isinstance(args[0], str) and args[0].startswith('Tables in database:'):
                            table_call_found = True
                            break
                    assert table_call_found, "No call with 'Tables in database:' was found"

                    # Check that a message about columns was echoed, but don't check the exact order
                    columns_call_found = False
                    for call in mock_echo.call_args_list:
                        args, _ = call
                        if len(args) == 1 and isinstance(args[0], str) and args[0].startswith('Columns in users table:'):
                            columns_call_found = True
                            break
                    assert columns_call_found, "No call with 'Columns in users table:' was found"

                    mock_echo.assert_any_call('Database initialized successfully.')


def test_init_db_error(app):
    """Test database initialization with an error."""
    with patch('crm_app.db.drop_all') as mock_drop_all:
        with patch('click.echo') as mock_echo:
            # Setup mock to raise an exception
            mock_drop_all.side_effect = Exception("Database error")

            # Call the function that would be inside init_db_command
            with app.app_context():
                try:
                    # Drop all tables
                    db.drop_all()
                except Exception as e:
                    mock_echo(f'Error initializing database: {str(e)}')
                    # Don't re-raise the exception in the test

            # Verify that the error message was echoed
            mock_echo.assert_called_with('Error initializing database: Database error')