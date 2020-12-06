from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

# Form used for logging in a user
class LoginForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
	password = StringField('password', validators=[InputRequired(), Length(min=10, max=50)])
	remember = BooleanField('remember')

# Form used for creating a new user form admin dashboard
class CreateUserForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
	password = StringField('password', validators=[InputRequired(), Length(min=10, max=50)])
	accountType = StringField('accountType', validators=[InputRequired(), Length(min=1, max=1)])
