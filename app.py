from flask import Flask, request, redirect, url_for, render_template, abort, make_response, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, validators
from flask_security import Security, PeeweeUserDatastore, login_required
from models import db, User, Role, UserRoles
import os

app = Flask("Foodr")
app.config["WTF_CSRF_ENABLED"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "insecure_key")
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = "email"
app.config["SECURITY_PASSWORD_HASH"] = "pbkdf2_sha512"
app.config["SECURITY_PASSWORD_SALT"] = app.config["SECRET_KEY"]

user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)

class LoginForm(FlaskForm):
	email = StringField('Email:', [validators.required()])
	password = PasswordField('Password:', [validators.required()])

def user_is_logged_in():
	return False

def user_exists(user_id):
	user = User.select().where(user_id == User.user_id)
	if len(user) == 1:
		print(user)
		return user
	return None

def get_user_information(user_id):
	return {"name": "Joel", "posts": 0, "diners": 0}

def picture_exists(picture_id):
	try:
		picture_id = int(picture_id)
		return True
	except ValueError:
		return False

@app.route("/")
@login_required
def home():
	return 'feed'

class PasswordForm(FlaskForm):
	password = PasswordField('password', [validators.required()])

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/picture/<picture_id>')
def picture(picture_id):
	if picture_exists(picture_id):
		return render_template(picture.html)
	else:
		abort(404)

@app.route('/user/<user_id>')
def user(user_id):
	if user_exists(user_id):
		user_information = get_user_information(user_id)
		return render_template('user.html', **user_information)
	else:
		abort(404)


class AccountForm(FlaskForm):
	name = StringField('name', [validators.InputRequired()])
	email = StringField('email', [validators.InputRequired()])
	age = IntegerField('age', [validators.InputRequired()])
	

@app.route('/create_account', methods=['GET', 'POST'])
def create_user():
	return render_template('create_account.html', form=form)


class GuestForm(FlaskForm):
	name = StringField('name', [validators.InputRequired()])
	email = StringField('email', [validators.InputRequired()])
	message = StringField('message', [validators.InputRequired()])

@app.route('/guest_book', methods=['get', 'post'])
def guest_book():
	if request.method == 'POST':	
		guest = Guest.create(name=request.form['name'], email=request.form['email'], message=request.form['message'])
		guests = Guest.select()
		return render_template('guests.html', guests=guests)
	else:
		form = GuestForm()
		return render_template('guest_book.html', form=form)

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
	app.run(debug=True)