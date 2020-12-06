from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
	password = StringField('password', validators=[InputRequired(), Length(min=10, max=50)])
	remember = BooleanField('remember')

class CreateUserForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
	password = StringField('password', validators=[InputRequired(), Length(min=10, max=50)])
	accountType = StringField('accountType', validators=[InputRequired(), Length(min=1, max=1)])


		#Length(min=1, max=1)])
