from flask import Flask, request, redirect, url_for, render_template, abort, make_response, session, flash
from flask_security import Security, login_required
from models import db, User, Role, UserRoles, Image
from auth import user_datastore, create_user
import os
import cloudinary
import cloudinary.uploader
from flask_security.core import current_user
import peewee
import math
from forms import RegisterForm, UploadForm
from pagination import page_range

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

@app.route('/user/<username>')
@app.route('/user/<username>/<page>')
def user_pageinate(username, page=1):
	try:
		images_per_page = 6
		user = User.select().where(User.username == username).get()
		page = int(page)
		all_images = Image.select().where(Image.user == user)
		images = all_images.order_by(Image.id).paginate(page, images_per_page)		
		last_page = math.ceil(len(all_images)/images_per_page) 
		if page > last_page and page != 1 or page <= 0:
			raise ValueError
		pagination = page_range(page, last_page)
		return render_template('user.html', user=user, images=images, current_page=page, pagination=pagination, last_page=last_page)
	except (IndexError, ValueError, peewee.DataError, User.DoesNotExist):
		abort(404)


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