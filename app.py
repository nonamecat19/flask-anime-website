from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# <-- database #
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class Title(db.Model):
    __tablename__ = "title"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    original_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image_name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(200), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    studio = db.Column(db.String(200), nullable=False)
    date_of_creating = db.Column(db.DateTime, default=datetime.utcnow())
    age_restriction = db.Column(db.Integer, nullable=False)
    movie_length = db.Column(db.String(200), nullable=False)
    star_count = db.Column(db.Integer, default=1)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship("Category", backref=db.backref("category", uselist=False))

    def __repr__(self):
        return f'<Title {self.name}>'

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(200), nullable=False)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.nickname}>'

class SelectedTitle(db.Model):
    __tablename__ = "selectedTitle"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("user", uselist=False))
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))
    title = db.relationship("Title", backref=db.backref("title", uselist=False))
    status = db.Column(db.String(200), nullable=False)
# --> #

# <-- links #
@app.route('/')
def index():
    sections = []
    categories = Category.query.all()
    for i in range(3):
        sections.append([categories[i], Title.query.filter_by(category_id=i+1).all()[:3]])
    return render_template('index.html', sections=sections)


@app.route('/anime-details/<int:id>')
def anime_details(id):
    title = Title.query.get_or_404(id)
    trends = Title.query.filter_by(category_id=3).all()
    # лайки б треба змінити
    likes = SelectedTitle.query.filter_by(title_id=id).all()
    count = 0
    for like in likes:
        if like.status != "закинуто":
            count += 1

    return render_template('anime-details.html', title=title, likes=count, trends=trends[:2])


@app.route('/categories')
def categories():
    sections = []
    categories = Category.query.all()
    for category in categories:
        titles = Title.query.filter_by(category_id=category.id).all()
        if len(titles) > 0:
            sections.append([category, titles])
    return render_template('categories.html', sections=sections)

@app.route('/contacts')
def blog():
    return render_template('blog-details.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/admin-panel')
def admin_panel():
    titles = Title.query.all()
    return render_template('admin-panel.html', titles=titles)

@app.route('/admin-panel/add-title', methods=["POST", "GET"])
def title_adding():
    categories = Category.query.all()
    if request.method == "POST":
        new_title = Title(name=request.form['title-name'], original_name=request.form['title-original_name'],
                          description=request.form['title-description'], image_name=request.form['title-image_name'],
                          type=request.form['title-type'], studio=request.form['title-studio'],
                          category_id=request.form.get('title-category'), age_restriction=request.form['title-age_restriction'],
                          movie_length=request.form['title-movie_length'], star_count=request.form['title-star_count'],
                          genres=request.form['title-genres'], status=request.form['title-status'])
        try:
            db.session.add(new_title)
            db.session.commit()
            return redirect("/admin-panel")
        except Exception as e:
            return str(e)
    return render_template('add-title.html', categories=categories)

@app.route('/admin-panel/delete-title/<int:id>')
def title_deleting(id):
    title = Title.query.get_or_404(id)
    try:
        db.session.delete(title)
        db.session.commit()
        return redirect("/admin-panel")
    except Exception as ex:
        return str(e)

@app.route('/admin-panel/update-title/<int:id>', methods=["POST", "GET"])
def title_updating(id):
    categories = Category.query.all()
    title = Title.query.get_or_404(id)
    if request.method == "POST":
        title.name = request.form['title-name']
        title.original_name = request.form['title-original_name']
        title.description = request.form['title-description']
        title.image_name = request.form['title-image_name']
        title.type = request.form['title-type']
        title.studio = request.form['title-studio']
        title.category_id = request.form.get('title-category')
        title.age_restriction = request.form['title-age_restriction']
        title.movie_length = request.form['title-movie_length']
        title.star_count = request.form['title-star_count']
        title.genres = request.form['title-genres']
        title.status = request.form['title-status']
        try:
            db.session.commit()
            return redirect("/admin-panel")
        except Exception as ex:
            return str(ex)
    return render_template('update-title.html', categories=categories, title=title)
# --> #

if __name__ == '__main__':
    app.run(debug=True)
