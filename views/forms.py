from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])

	
class EditForm(Form):
	username = StringField('username', validators=[DataRequired()])
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

