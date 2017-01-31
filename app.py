from flask import Flask, render_template
app = Flask("Svetsr")
visits = 0

@app.route("/")
def home():
	global visits
	visits += 1
	return render_template('home.html', visits=visits, username="Joel")

@app.route('/about/')
def about():
	return render_template('about.html')

if __name__ == "__main__":
	app.run(debug=True)