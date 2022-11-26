from app import db, Title, Category, User, Comment

db.session.add(Category(name="Новинки"))
db.session.add(Category(name="Популярні"))
db.session.add(Category(name="В тренді"))
db.session.add(Category(name="Романтика"))
db.session.add(Category(name="Фентезі"))
db.session.add(User(nickname="адмін", login="admin", password="admin"))
db.session.add(Title(name="Боруто", original_name="boruto", description="Ipsum", image_name="live-1.jpg",
                type="серіал", studio="Mappa", category_id=1, age_restriction=16, movie_length="20хв/серія",
                star_count=4, genres="фантастика, бойовик, пригоди", status="онгоїнг"))
db.session.add(Title(name="Атака титанів", original_name="shingeki no koujin", description="Ipsum Ipsum Ipsum Ipsum Ipsum Ipsum", image_name="trend-4.jpg",
                type="серіал", studio="Mappa", category_id=1, age_restriction=16, movie_length="20хв/серія",
                star_count=5, genres="фантастика, бойовик, пригоди", status="онгоїнг"))
db.session.add(Title(name="Сао", original_name="sword art online", description="Ipsum", image_name="popular-3.jpg",
                type="серіал", studio="Mappa", category_id=2, age_restriction=16, movie_length="20хв/серія",
                star_count=4, genres="фантастика, бойовик, пригоди", status="онгоїнг"))
db.session.add(Title(name="Обіцяний Неверленд", original_name="the promised neverlend", description="Ipsum",
                     image_name="popular-3.jpg", type="серіал", studio="Lis", category_id=3, age_restriction=16,
                     movie_length="20хв/серія", star_count=4, genres="пригоди", status="онгоїнг"))

db.session.add(Comment(user_id=1, title_id=1, comment="Шось дуже круте"))

db.session.commit()