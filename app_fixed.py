from crm_app import create_app, db
from crm_app.models import User, Customer, Deal, Activity
import click
from flask.cli import with_appcontext

app = create_app()

@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    try:
        # Drop all tables
        db.drop_all()
        click.echo('Dropped all tables.')

        # Create all tables
        db.create_all()
        click.echo('Created all tables.')

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        click.echo(f'Tables in database: {", ".join(tables)}')

        # Verify User table columns
        columns = [col['name'] for col in inspector.get_columns('users')]
        click.echo(f'Columns in users table: {", ".join(columns)}')

        click.echo('Database initialized successfully.')
    except Exception as e:
        click.echo(f'Error initializing database: {str(e)}')
        raise

@app.cli.command('create-admin')
@with_appcontext
def create_admin():
    """Create an admin user."""
    admin = User(username='admin', email='admin@example.com')
    admin.set_password('password')
    db.session.add(admin)
    db.session.commit()
    click.echo('Created admin user.')

@app.cli.command('seed-data')
@with_appcontext
def seed_data():
    """Seed the database with sample data."""
    # Create sample customers
    customers = [
        Customer(name='John Smith', email='john.smith@example.com', phone='+1 (234) 567-890',
                company='Acme Corp', status='Active',
                address='123 Main St, San Francisco, CA 94105',
                notes='Key decision maker. Prefers email communication.'),
        Customer(name='Sarah Johnson', email='sarah.johnson@example.com', phone='+1 (345) 678-901',
                company='TechStart Inc', status='Pending',
                address='456 Market St, San Francisco, CA 94105',
                notes='New lead from conference.'),
        Customer(name='Michael Chen', email='michael.chen@example.com', phone='+1 (456) 789-012',
                company='Global Solutions', status='Active',
                address='789 Mission St, San Francisco, CA 94105',
                notes='Interested in enterprise package.')
    ]
    db.session.add_all(customers)
    db.session.commit()

    # Create sample deals
    deals = [
        Deal(name='Enterprise License', value=75000, stage='Qualification', probability=30,
             customer_id=1, description='Annual enterprise license for 100 users.'),
        Deal(name='Consulting Services', value=120000, stage='Proposal', probability=60,
             customer_id=2, description='3-month consulting project.'),
        Deal(name='Software Implementation', value=200000, stage='Closing', probability=90,
             customer_id=3, description='Full software implementation with training.')
    ]
    db.session.add_all(deals)
    db.session.commit()

    # Create sample activities
    activities = [
        Activity(type='Created', description='Deal created', deal_id=1),
        Activity(type='Call', description='Initial discovery call with client', deal_id=1),
        Activity(type='Email', description='Sent proposal', deal_id=2),
        Activity(type='Meeting', description='Product demo', deal_id=3)
    ]
    db.session.add_all(activities)
    db.session.commit()

    click.echo('Added sample data.')

@app.shell_context_processor
def make_shell_context():
    """Make variables available in the shell context."""
    return {'db': db, 'User': User, 'Customer': Customer, 'Deal': Deal, 'Activity': Activity}

if __name__ == '__main__':
    app.run(debug=True)