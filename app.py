from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
#
#
# class App(db.model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/anime-details')
def anime_details():
    return 'Hello World!'


@app.route('/anime-watching')
def anime_watching():
    return 'Hello World!'


# @app.route('/blog')
@app.route('/')
def blog():
    return render_template('blog.html')


@app.route('/blog-details')
def blog_details():
    return 'Hello World!'


@app.route('/categories')
def categories():
    return 'Hello World!'


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
