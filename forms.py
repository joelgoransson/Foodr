from wtforms import StringField, IntegerField, PasswordField,validators, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields.html5 import EmailField


class UploadForm(FlaskForm):
    file = FileField()

class RegisterForm(FlaskForm):
	def validate_username(form, field):
		if len(User.select().where(field.data.lower() == User.username)):
			raise ValidationError('Username already exist!')
	def validate_email(form, field):
		if len(User.select().where(field.data == User.email)):
			raise ValidationError('Email is already in use!')

	username = StringField('username', [validators.InputRequired()], description="Username")
	email = EmailField('email',[validators.InputRequired()], description="Email")
	password = PasswordField('password', [validators.InputRequired(), validators.length(min=8,message='Password must be at least 8 characters long.'), validators.EqualTo('retype_password', message='Passwords must match.')], description="Password")
	retype_password = PasswordField('retype_password', [validators.InputRequired()], description="Retype Password")
