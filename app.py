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
    return render_template('anime-details.html')


@app.route('/anime-watching')
def anime_watching():
    return 'Hello World!'


@app.route('/blog')
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
    return render_template('signup.html')


@app.route('/admin-panel')
def admin_panel():
    return render_template('admin-panel.html')


if __name__ == '__main__':
    app.run(debug=True)
