from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length

class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional(), Length(max=200)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save')