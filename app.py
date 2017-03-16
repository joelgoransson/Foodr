from flask import Flask, request, redirect, url_for, render_template, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
import os
import uuid
app = Flask("Foodr")
app.config["WTF_CSRF_ENABLED"] = False

base = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(base, 'static', 'uploads')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class LoginForm(FlaskForm):
	email = StringField('Email:', [validators.required()])
	password = PasswordField('Password:', [validators.required()])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/picture/upload', methods=['GET', 'POST'])
def upload_file():
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
        	filename, file_extension = os.path.splitext(file.filename)
        	file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + file_extension))
        	return redirect(url_for('upload_file', filename=filename))
    return render_template("upload.html")


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

@app.route('/contact', methods=['get', 'post'])
def contact():
	if request.method == 'POST':	
		return 'yay'
	else:
		return render_template('contact.html')
if __name__ == "__main__":
	#app.run("0.0.0.0", debug=True)
	app.run(debug=True)