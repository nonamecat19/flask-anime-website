from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# тут має бути дуже складний секретний ключ для сесій
app.config['SECRET_KEY'] = '1111'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


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


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("user", uselist=False))
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))
    title = db.relationship("Title", backref=db.backref("title", uselist=False))
    date_of_creating = db.Column(db.DateTime, default=datetime.utcnow())
    comment = db.Column(db.String(1000), nullable=False)


@app.route('/')
def index():
    sections = []
    categories = Category.query.all()
    for i in range(3):
        sections.append([categories[i], Title.query.filter_by(category_id=i + 1).all()[:3]])

    carousel_items = [ {'image': "bg-1.jpg", 'title': "Доля / Ніч битви: Світ нескінченних клинків", 'desc': "Мандруючи світом вже понад 30-ти днів..."},
                       {'image': "bg-2.jpg", 'title': "Клинок, розсікаючий демонів", 'desc': "Життя перевернулося з ніг на голову, коли його спіткала трагедія..."}]
    return render_template('index.html', sections=sections, carousel_items=carousel_items)


@app.route('/anime-details/<int:id>', methods=["POST", "GET"])
def anime_details(id):
    title = Title.query.get_or_404(id)
    trends = Title.query.filter_by(category_id=1).all()
    comments = Comment.query.filter_by(title_id=id).all()

    if request.method == "POST":
        new_comment = Comment(user_id=session['auth_id'], title_id=id, date_of_creating=datetime.now(),
                              comment=request.form['comment-content'])
        try:
            db.session.add(new_comment)
            db.session.commit()
            return redirect(f"/anime-details/{id}")
        except Exception as e:
            return str(e)

    return render_template('anime-details.html', title=title, trends=trends[:2], comments=comments, comment_length=len(comments))


@app.route('/categories')
def categories():
    sections = []
    categories = Category.query.all()
    for category in categories:
        titles = Title.query.filter_by(category_id=category.id).all()
        if len(titles) > 0:
            sections.append([category, titles])
    return render_template('categories.html', sections=sections)


@app.route('/login', methods=["POST", "GET"])
def login():
    message = ""
    if request.method == "POST":

        users = User.query.all()
        if users[0].login == request.form['user-login'] and users[0].password == request.form['user-password']:
            # дані передаються в сесію
            session['admin'] = True
            session['user'] = False
            session['auth'] = True
            session['auth_id'] = '1'
            return redirect("/admin-panel")
        for user in users:
            if user.login == request.form['user-login'] and user.password == request.form['user-password']:
                # дані передаються в сесію
                session['user'] = True
                session['admin'] = False
                session['auth'] = True
                session['auth_id'] = str(user.id)
                return redirect(f"/profile/{user.id}")
        message = "Неправильно введений логін чи пароль"
    return render_template('login.html', message=message)


@app.route('/signup', methods=["POST", "GET"])
def signup():
    message = ""
    if request.method == "POST":
        user_exists = User.query.filter_by(login=request.form['user-login']).first()
        if user_exists:
            message = "Логін зайнято"
        else:
            new_user = User(login=request.form['user-login'], nickname=request.form['user-nickname'],
                            password=request.form['user-password'])
            try:
                db.session.add(new_user)
                db.session.commit()

                session['user'] = True
                session['admin'] = False
                session['auth'] = True
                session['auth_id'] = str(new_user.id)
                return redirect(f"/profile/{new_user.id}")

            except Exception as e:
                return str(e)

    return render_template('signup.html', message=message)


@app.route('/admin-panel')
def admin_panel():
    if 'admin' not in session or not session['admin']:
        # редірект на іншу сторінку якщо хоче зайти в адмінку не адмін
        return redirect('/')

    titles = Title.query.all()
    users = User.query.all()
    categories = Category.query.all()
    comments = Comment.query.all()
    activities = {}

    def getCategoryActivity(category_id):
        for title in titles:
            if title.category_id == category_id:
                return True
        return False

    for category in categories:
        activities[category.id] = getCategoryActivity(category.id)

    return render_template('admin-panel.html', titles=titles, categories=categories, activities=activities, users=users, comments=comments)


@app.route('/admin-panel/add-title', methods=["POST", "GET"])
def title_adding():
    if 'admin' not in session or not session['admin']:
        # редірект на іншу сторінку якщо хоче зайти в адмінку не адмін
        return redirect('/')

    categories = Category.query.all()
    if request.method == "POST":
        new_title = Title(name=request.form['title-name'], original_name=request.form['title-original_name'],
                          description=request.form['title-description'], image_name=request.form['title-image_name'],
                          type=request.form['title-type'], studio=request.form['title-studio'],
                          category_id=request.form.get('title-category'),
                          age_restriction=request.form['title-age_restriction'],
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
    if 'admin' not in session or not session['admin']:
        # редірект на іншу сторінку якщо хоче зайти в адмінку не адмін
        return redirect('/')

    title = Title.query.get_or_404(id)
    comments = Comment.query.filter_by(title_id=id).all()
    try:
        db.session.delete(title)
        for comment in comments:
            db.session.delete(comment)
        db.session.commit()
        return redirect("/admin-panel")
    except Exception as ex:
        return str(ex)


@app.route('/admin-panel/update-title/<int:id>', methods=["POST", "GET"])
def title_updating(id):
    if 'admin' not in session or not session['admin']:
        # редірект на іншу сторінку якщо хоче зайти в адмінку не адмін
        return redirect('/')

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


@app.route('/admin-panel/add-category', methods=["POST", "GET"])
def category_adding():
    if 'admin' not in session or not session['admin']:
        # редірект на іншу сторінку якщо хоче зайти в адмінку не адмін
        return redirect('/')

    if request.method == "POST":
        new_category = Category(name=request.form['category-name'])
        try:
            db.session.add(new_category)
            db.session.commit()
            return redirect("/admin-panel")
        except Exception as e:
            return str(e)
    return render_template('add-category.html')


@app.route('/admin-panel/delete-category/<int:id>')
def category_deleting(id):
    if 'admin' not in session or not session['admin']:
        # редірект на іншу сторінку якщо хоче зайти в адмінку не адмін
        return redirect('/')

    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        return redirect("/admin-panel")
    except Exception as ex:
        return str(ex)


@app.route('/admin-panel/update-category/<int:id>', methods=["POST", "GET"])
def category_updating(id):
    if 'admin' not in session or not session['admin']:
        # редірект на іншу сторінку якщо хоче зайти в адмінку не адмін
        return redirect('/')

    category = Category.query.get_or_404(id)
    if request.method == "POST":
        category.name = request.form['category-name']
        try:
            db.session.commit()
            return redirect("/admin-panel")
        except Exception as ex:
            return str(ex)
    return render_template('update-category.html', category=category)


@app.route('/profile/<int:id>', methods=["POST", "GET"])
def profile(id):
    # перевірка чи користувач входить саме до свого профілю
    if int(session['auth_id']) != int(id):
        # редірект на іншу сторінку якщо хоче до чужого
        return redirect('/')

    # натиснута кнопка вийти з аккаунта
    if request.method == "POST":
        # очищається сесія від даних
        session.clear()
        # редірект на головну
        return redirect('/')

    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)


@app.route('/profile/delete/<int:id>')
def profile_deleting(id):
    user = User.query.get_or_404(id)
    comments = Comment.query.filter_by(user_id=id).all()
    try:
        session.clear()
        db.session.delete(user)
        for comment in comments:
            db.session.delete(comment)
        db.session.commit()
        return redirect('/')
    except Exception as ex:
        return str(ex)

@app.route('/admin-panel/delete-comment/<int:id>')
def comment_deleting(id):
    comment = Comment.query.get_or_404(id)
    try:
        db.session.delete(comment)
        db.session.commit()
        return redirect('/admin-panel')
    except Exception as ex:
        return str(ex)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
