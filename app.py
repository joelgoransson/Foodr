from flask import Flask, request, redirect, url_for, render_template, abort, make_response, session, flash
from flask_wtf.file import FileField
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField,validators, ValidationError
from wtforms.fields.html5 import EmailField
from flask_security import Security, login_required
from models import db, User, Role, UserRoles, Image
from auth import user_datastore, create_user
import os
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename
from flask_security.core import current_user
import json
import peewee
import math

app = Flask("Foodr")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "insecure_key")
app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = "email"
app.config["SECURITY_PASSWORD_HASH"] = "pbkdf2_sha512"
app.config["SECURITY_PASSWORD_SALT"] = app.config["SECRET_KEY"]

cloudinary.config(
	cloud_name = os.environ.get("cloudinary_name"),
	api_key = os.environ.get('cloudinary_key'),
	api_secret = os.environ.get('cloudinary_secret')
)

security = Security(app, user_datastore)
@app.route("/")
@login_required
def home():
	return render_template('feed.html')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
class UploadForm(FlaskForm):
    file = FileField()
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		file = form.file.data
		if file == None:
			return 'error'
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			cloudinary_image = cloudinary.uploader.upload(file)
			image = Image(url=cloudinary_image["url"], user=current_user.id)
			image.save()
			return redirect("image/" + str(image.id))
	else:
		return render_template('upload.html', form=form)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/image/<image_id>')
def picture(image_id):
	image = Image.select().where(Image.id == image_id)
	try:
		return render_template('image.html', image=image[0])
	except (IndexError, ValueError):
		abort(404)

TOTAL_IMAGES_PER_PAGE = 1
@app.route('/user/<username>')
def user(username):
	user = User.select().where(User.username == username).get()
	try:
		all_images = Image.select().where(Image.user == user)
		images = all_images.where(Image.user == user).order_by(Image.id).paginate(0, TOTAL_IMAGES_PER_PAGE)
		last_page = math.ceil(len(all_images)/TOTAL_IMAGES_PER_PAGE)
		
		pages = last_page
		if pages > 5:
			pages = 5
		pagination = []
		for p in range(pages):
			pagination.append(p + 1)
		return render_template('user.html', user=user, images=images, current_page=1, pagination=pagination, last_page=last_page)
	except (IndexError, ValueError):
		abort(404)


@app.route('/user/<username>/<page>')
def user_pageinate(username, page):
	user = User.select().where(User.username == username).get()
	try:
		page = int(page)
		all_images = Image.select().where(Image.user == user)
		images = all_images.order_by(Image.id).paginate(page, TOTAL_IMAGES_PER_PAGE)
		
		last_page = math.ceil(len(all_images)/TOTAL_IMAGES_PER_PAGE) 
		first_page = 1

		count = 0
		start = page
		end = page
		done = [0, 0]
		while count <= 3:
			if start > first_page:
				start -= 1
				count += 1
			else:
				done[0] = True

			if end < last_page:
				end += 1
				count += 1
			else:
				done[1] = True

			if done[0] and done[1]:
				break
		pagination = []
		for p in range(start, end + 1):
			pagination.append(p)

		if not images or not page or page == 1:
			return redirect("user/"+username)
		return render_template('user.html', user=user, images=images, current_page=page, pagination=pagination, last_page=last_page)
	except (IndexError, ValueError, peewee.DataError):
		abort(404)


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

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if current_user.is_authenticated:
		return redirect('/')
	else:
		if form.validate_on_submit():
			try: 
				create_user(form.email.data, form.username.data.lower(), form.password.data)
			except (peewee.IntegrityError):
				abort(500)
			return redirect(url_for("user", username=form.username.data.lower()))
		else:
			return render_template('register.html', form=form)

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)
	app.run(debug=True)