from flask import Flask, render_template, abort
app = Flask("Foodr")
visits = 0

def user_exists(user_id):
	try:
		user_id = int(user_id)
		return True
	except:
		return False

def picture_exists(picture_id):
	try:
		picture_id = int(picture_id)
		return True
	except ValueError:
		return False

@app.route("/")
def home():
	global visits
	visits += 1
	return render_template('home.html', visits=visits, username="Joel")

@app.route('/about/')
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
		return render_template('user.html', user_id=user_id, username = user_id)
	else:
		abort(404)

if __name__ == "__main__":
	app.run(debug=True)