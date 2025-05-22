from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from crm_app.models import User, Customer
from sqlalchemy.exc import OperationalError
from datetime import datetime

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        try:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken. Please choose a different one.')
        except OperationalError:
            # If the table doesn't exist yet, we can't validate
            pass

    def validate_email(self, email):
        try:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already registered. Please use a different one.')
        except OperationalError:
            # If the table doesn't exist yet, we can't validate
            pass

class CustomerForm(FlaskForm):
    """Form for creating and updating customers"""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Length(max=20)])
    company = StringField('Company', validators=[Length(max=100)])
    address = StringField('Address', validators=[Length(max=200)])
    status = SelectField('Status', choices=[
        ('New', 'New'), 
        ('Active', 'Active'), 
        ('Inactive', 'Inactive'),
        ('Pending', 'Pending')
    ])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save')
    
    def validate_email(self, email):
        # Only check for duplicates when creating a new customer or changing email
        if hasattr(self, 'customer_id') and self.customer_id.data:
            customer = Customer.query.filter_by(email=email.data).first()
            if customer and customer.id != int(self.customer_id.data):
                raise ValidationError('Email is already registered to another customer.')
        else:
            customer = Customer.query.filter_by(email=email.data).first()
            if customer:
                raise ValidationError('Email is already registered to another customer.')

class DealForm(FlaskForm):
    """Form for creating and updating deals"""
    name = StringField('Deal Name', validators=[DataRequired(), Length(max=100)])
    customer_id = SelectField('Customer', validators=[DataRequired()])
    value = FloatField('Value ($)', validators=[DataRequired()])
    stage = SelectField('Stage', choices=[
        ('Qualification', 'Qualification'),
        ('Proposal', 'Proposal'),
        ('Negotiation', 'Negotiation'),
        ('Closing', 'Closing'),
        ('Closed Won', 'Closed Won'),
        ('Closed Lost', 'Closed Lost')
    ])
    probability = SelectField('Probability', choices=[
        ('10', '10%'), ('20', '20%'), ('30', '30%'), ('40', '40%'), ('50', '50%'),
        ('60', '60%'), ('70', '70%'), ('80', '80%'), ('90', '90%'), ('100', '100%')
    ])
    close_date = DateField('Expected Close Date', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class ActivityForm(FlaskForm):
    """Form for creating deal activities"""
    type = SelectField('Activity Type', choices=[
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('Meeting', 'Meeting'),
        ('Note', 'Note'),
        ('Task', 'Task')
    ])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.today)
    submit = SubmitField('Add Activity')

class ContactForm(FlaskForm):
    """Form for contact us page"""
    name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    company = StringField('Company Name', validators=[Length(max=100)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    subject = SelectField('Subject', choices=[
        ('General Inquiry', 'General Inquiry'),
        ('Product Demo', 'Request a Demo'),
        ('Technical Support', 'Technical Support'),
        ('Pricing', 'Pricing Information'),
        ('Partnership', 'Partnership Opportunity'),
        ('Other', 'Other')
    ])
    message = TextAreaField('Your Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')