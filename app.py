import datetime

from flask import Flask, render_template, request
from werkzeug.utils import redirect

from data import db_session
from data.books import Books
from data.first_book import books
from data.search import search
from data.blueprint_login import blueprint_login
from data.blueprint_profile import blueprint_profile
from data.blueprint_register import blueprint_register
from data.blueprint_cart import blueprint_cart
from flask_login import LoginManager, login_required, logout_user
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Z,kjrjTds_secret_key'
app.register_blueprint(books, url_prefix="/book")
app.register_blueprint(search, url_prefix="/search")
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(blueprint_profile, name="profile")
app.register_blueprint(blueprint_register, name="register")
app.register_blueprint(blueprint_login, name="login")
app.register_blueprint(blueprint_cart, name="cart")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        db_session.global_init("db/users_data.db")
        db_sess = db_session.create_session()

        recommendations_list = []
        for book in db_sess.query(Books).filter(Books.rating > 0.9):
            recommendations_list.append((book.content, book.image, f'book/{book.id}'))

        value_novelties = datetime.date.today() - datetime.timedelta(
            days=30)
        date = datetime.timedelta(days=30)

        novelties_list = []
        for book in db_sess.query(Books).filter(
                (Books.created_date - value_novelties) <= date):
            novelties_list.append((book.content, book.image,
                                   book.created_date, f'book/{book.id}'))

        novelties_list.sort(reverse=True, key=lambda x: x[2])
        novelties_list = novelties_list[:5]
        numbers_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "11+"]

        primary_school_list = []
        for book in db_sess.query(Books).filter((Books.limitation ==
                                                 "Начальная школа") |
                                                (Books.limitation.in_(
                                                    numbers_list[:3]))):
            primary_school_list.append((book.content, book.image, f'book/{book.id}'))

        secondary_school_list = []
        for book in db_sess.query(Books).filter((Books.limitation ==
                                                 "Средняя школа") |
                                                (Books.limitation.in_(
                                                    numbers_list[4:8]))):
            secondary_school_list.append((book.content, book.image, f'book/{book.id}'))

        high_school_list = []
        for book in db_sess.query(Books).filter((Books.limitation ==
                                                 "Старшая школа") |
                                                (Books.limitation.in_(
                                                    numbers_list[9:10]))):
            high_school_list.append((book.content, book.image, f'book/{book.id}'))

        students_list = []
        for book in db_sess.query(Books).filter((Books.limitation ==
                                                 "Студентам") |
                                                (Books.limitation ==
                                                 (numbers_list[-1]))):
            students_list.append((book.content, book.image, f'book/{book.id}'))

        return render_template("index.html",
                               recommendations_list=recommendations_list,
                               novelties_list=novelties_list,
                               primary_school_list=primary_school_list,
                               secondary_school_list=secondary_school_list,
                               high_school_list=high_school_list,
                               students_list=students_list)
    elif request.method == "POST":
        text = request.form['search'].replace(' ', '%')
        return redirect(f"/search/{text}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
