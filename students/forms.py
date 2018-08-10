from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class AssignmentsForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    details = StringField('Details', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    teacher = StringField('Teacher', validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    submit = SubmitField('Add')

class AssesmentsForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    details = StringField('Details', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    teacher = StringField('Teacher', validators=[DataRequired()])
    submit = SubmitField('Add')