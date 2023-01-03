from markupsafe import escape
from dateutil import tz
from datetime import datetime
from flask import Flask, abort, render_template, request, url_for, flash, redirect, abort
from forms import CourseForm
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '5171360bfd5a545303dae3fd654ca239ab8880bc89e0e585'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

messages = [{'title': 'Message One',
            'content': 'Message One Content'},
            {'title': 'Message Two',
            'content': 'Message Two Content'}
            ]

courses_list = [{
    'title': 'Python 101',
    'description': 'Learn Python basics',
    'price': 34,
    'available': True,
    'level': 'Beginner'
    }]

@app.route('/index/')
@app.route('/')
def hello():
    try:
        return render_template('index.html', currentTime=datetime.now(tz=tz.tzlocal()))
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

    return render_template('messages.html', messages=messages)


# ...

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('posts'))

    return render_template('create.html')

@app.route('/form/', methods=('GET','POST'))
def form():    
    form = CourseForm()
    if form.validate_on_submit():
        courses_list.append({'title': form.title.data,
                             'description': form.description.data,
                             'price': form.price.data,
                             'available': form.available.data,
                             'level': form.level.data
                             })
        return redirect(url_for('courses'))
    return render_template('form.html', form=form)

@app.route('/courses/')
def courses():
    return render_template('courses.html', courses_list=courses_list)

@app.route('/posts/')
def posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)

# ...

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)