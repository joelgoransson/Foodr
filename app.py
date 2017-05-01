from flask import Flask, request, redirect, url_for, render_template, abort, make_response, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, validators
from models import db, Guest
import os

app = Flask("Foodr")
app.config["WTF_CSRF_ENABLED"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "insecure_key")

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

class LoginForm(FlaskForm):
	email = StringField('Email:', [validators.required()])
	password = PasswordField('Password:', [validators.required()])

def user_is_logged_in():
	return False

def user_exists(user_id):
	try:
		user_id = int(user_id)
		return True
	except:
		return False

def get_user_information(user_id):
	return {"name": "Joel", "posts": 0, "diners": 0}

def picture_exists(picture_id):
	try:
		picture_id = int(picture_id)
		return True
	except ValueError:
		return False

@app.route("/")
def home():
	if user_is_logged_in():
		pass #return feed
	else:
		form = LoginForm()
		if form.validate_on_submit(): #add login validation
			pass #login in
		else:
			return render_template('login.html', form=form)

@app.route('/easter_egg/have/i/visited/this/page/before')
def have_i_visited_this_page_before():
	try:
		visited = int(request.cookies.get('visited', "0"))
	except ValueError:
		visited = 0
	if visited == 0:
		response = make_response('no.')
		response.set_cookie('visited', "1")
	else:
		response = make_response('yes.')
	return response

class PasswordForm(FlaskForm):
	password = PasswordField('password', [validators.required()])

@app.route('/easter_egg/secret_page', methods=['POST', 'GET'])
def secret_page():
	logged_in = int(session.get("logged_in", "0"))
	form = PasswordForm()
	if request.method == 'POST':
		if request.form['password'] == 'hallonsylt':
			return "that's correct!"
		return render_template('secret_page_form.html', form=form, error="Wrong password!")
	else:
		if logged_in == "1":
			return 'Welcome to my top secret page!'
		else:
			return render_template('secret_page_form.html', form=form, error=None)
		

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