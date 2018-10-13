from flask import Flask, request
from flask import render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index/<name>')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/about')
def about(name=None):
	return render_template('about.html', name=name)

@app.route('/generator', methods=['GET', 'POST'])
def generator(name=None):
	params = ['Red', 'Blue', 'Black', 'Orange']
	error1 = "The departure and arrival airports may not be the same."
	error2 = "Please enter a value for passengers."
	if request.method == 'POST':
		passengers = request.form['passengers']
		departure = request.form['dept']
		arrival = request.form['arr']
		if departure == arrival:
			return render_template('generator.html', params=params, error=error1)
		if passengers is '':
			return render_template('generator.html', params=params, error=error2)

		results = query(passengers, departure, arrival)
		total=999 #dummy variable
		return render_template('generator.html', params=params, error="", results=results, total=total)

	else:
		return render_template('generator.html', params=params, error="")


def query(passengers, departure, arrival):
	results = [[180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100],
				[180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100]]
	return results