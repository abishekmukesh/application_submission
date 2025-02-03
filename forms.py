from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import re

def validate_roll_number(form, field):
  roll_number = field.data
  if not re.match(r'^IITM-\d{10}$', roll_number):
    raise ValidationError("Roll number must be in the format IITM-XXXXXXXXXX where X is a 10 digit number")

def validate_gmail(form, field):
    email = field.data
    if not email.endswith('@gmail.com'):
        raise ValidationError('Email must end with @gmail.com')
def validate_phone_number(form, field):
   phone = field.data
   if not re.match(r'^\d{10}$', phone):
     raise ValidationError('Phone number must be 10 digits long.')


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentLoginForm(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentSignupForm(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired(),validate_roll_number])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Signup')


class ApplicationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(),validate_gmail])
    phone = StringField('Phone Number', validators=[DataRequired(),validate_phone_number])
    degree = StringField('Degree', validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    id_proof = FileField('ID Proof (PDF, JPG, PNG)', validators=[])
    degree_certificate = FileField('Degree Certificate (PDF, JPG, PNG)', validators=[])
    submit = SubmitField('Submit Application')


class AdminReviewForm(FlaskForm):
    status = SelectField('Status', choices=[('Approved', 'Approve'), ('Rejected', 'Reject')])
    submit = SubmitField('Update')