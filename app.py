from markupsafe import escape
from dateutil import tz
from datetime import datetime
from flask import Flask, abort, render_template

app = Flask(__name__)

@app.route('/index/')
@app.route('/')
def hello():
	try:
		return render_template('index.html', currentTime = datetime.now(tz=tz.tzlocal()))
	except:
		return render_template('error.html')

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/capitalize/<word>/')
def capitalize(word):
	return '<h1>{}</h1>'.format(escape(word.capitalize()))

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1, n2):
	return '<h1>{}</h1>'.format(n1 + n2)

@app.route('/users/<int:user_id>/')
def greet_user(user_id):
	users = ['Bob', 'Jane', 'Adam']
	try:
		return '<h2>Hi {}</h2>'.format(users[user_id])
	except IndexError:
		abort(404)

@app.route('/comments/')
def comments():
	comments = [
				'comment one',
				'comment two',
				'comment three',
				'comment four'
				]
	return render_template('comments.html', comments=comments)

@app.route('/messages/')
def messages():

	messages = [{'title': 'Message One',
				'content': 'Message One Content'},
				{'title': 'Message Two',
				'content': 'Message Two Content'}
				]

	return render_template('messages.html', messages=messages)