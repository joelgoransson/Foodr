from flask import Flask, request, redirect, url_for, render_template, abort, make_response, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, validators
from flask_security import Security, PeeweeUserDatastore, login_required
from models import db, User, Role, UserRoles
import os
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename

app = Flask("Foodr")
app.config["WTF_CSRF_ENABLED"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "insecure_key")
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = "email"
app.config["SECURITY_PASSWORD_HASH"] = "pbkdf2_sha512"
app.config["SECURITY_PASSWORD_SALT"] = app.config["SECRET_KEY"]

cloudinary.config(
	cloud_name = os.environ.get("cloudinary_name"),
	api_key = os.environ.get('cloudinary_key'),
	api_secret = os.environ.get('cloudinary_secret')
)

user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)

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

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			image = cloudinary.uploader.upload(file)
			return "Uploaded image"
	else:
		return '''
			<!doctype html>
	    	<title>Upload new File</title>
	    	<h1>Upload new File</h1>
	    	<form method=post enctype=multipart/form-data>
	     	<p><input type=file name=file>
	        	 <input type=submit value=Upload>
	    	</form>

	   	'''

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/picture/<picture_id>')
def picture(picture_id):
	if picture_exists(picture_id):
		return render_template(picture.html)
	else:
		abort(404)

@app.route('/user/<user_profile>')
def user(user_profile):
	if user_profile.isdigit():
		user = User.select().where(User.id == user_profile)
	else:
		user = User.select().where(User.username == user_profile)
	
	try:
		return render_template('user.html', user=user[0])
	except IndexError:
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