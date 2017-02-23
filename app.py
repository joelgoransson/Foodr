from flask import Flask, request, redirect, url_for, render_template, abort
import os
import uuid
app = Flask("Foodr")

base = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(base, 'static', 'uploads')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
	return True

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
	return render_template('login.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/picture/<picture_id>')
def picture(picture_id):
	if picture_exists(picture_id):
		return "It works"
	else:
		abort(404)


@app.route('/user/<user_id>')
def user(user_id):
	if user_exists(user_id):
		user_information = get_user_information(user_id)
		return render_template('user.html', **user_information)
	else:
		abort(404)

@app.route('/homework')
def homework():
	return render_template('homework.html')

@app.route('/message', methods=['POST'])
def message():
	return 'You posted it!'

@app.route('/addition', methods=['POST'])
def addition():
	try:
		number1 = int(request.form['number1'])
		number2 = int(request.form['number2'])
		return str(number1 + number2)
	except ValueError:
		return 'Something went wrong!'

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)