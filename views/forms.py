from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from models.model import User

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = StringField('password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(username=self.username.data).first()
		if user != None:
			self.username.errors.append('This username is already in use. Please choose another one.')
			return False
		user = User.query.filter_by(email=self.email.data).first()
		if user != None:
			self.email.errors.append('This email is already in use. Please use another one.')
			return False

		return True

class EditForm(Form):
	username = StringField('username', validators=[DataRequired()])
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

	def __init__(self, original_username, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_username = original_username

	def validate(self):
		if not Form.validate(self):
			return False
		if self.username.data == self.original_username:
			return True

		user = User.query.filter_by(username=self.username.data).first()
		if user != None:
			self.username.errors.append('This username is already in use. Please choose another one.')
			return False

		return True

