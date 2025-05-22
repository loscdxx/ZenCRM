from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from wtforms.widgets import NumberInput

class DealForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    value = FloatField('Value ($)', validators=[DataRequired(), NumberRange(min=0)], widget=NumberInput(step='0.01'))
    probability = IntegerField('Probability (%)', validators=[DataRequired(), NumberRange(min=0, max=100)], default=50)
    expected_close_date = DateField('Expected Close Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Open', 'Open'), ('Won', 'Won'), ('Lost', 'Lost')], default='Open')
    notes = TextAreaField('Notes', validators=[Optional()])
    customer_id = SelectField('Customer', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Save')