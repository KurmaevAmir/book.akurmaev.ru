import datetime

from flask import Flask, render_template, request, session
from werkzeug.utils import redirect

from data import db_session
from data.SendEmail.blueprint_email_confirmation import confirmation
from data.blueprint_add_book import add_book
from data.blueprint_add_cloud import add_cloud
from data.books import Books
from data.data_to_save import UPLOAD_FOLDER
from data.blueprint_book import blueprint_book
from data.search import search
from data.blueprint_login import blueprint_login
from data.blueprint_profile import blueprint_profile
from data.blueprint_register import blueprint_register
from data.blueprint_cart import blueprint_cart
from data.blueprint_cart_add import blueprint_cart_add
from data.blueprint_cart_delete import blueprint_cart_delete
from data.blueprint_booking import blueprint_booking
from data.blueprint_information import blueprint_information
from data.blueprint_cloud import cloud
from flask_login import LoginManager
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Z,kjrjTds_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

app.register_blueprint(blueprint_book, url_prefix="/book")
app.register_blueprint(search, url_prefix="/search")
app.register_blueprint(add_book, url_prefix="/add_book")
app.register_blueprint(add_cloud, url_prefix="/add_cloud")
app.register_blueprint(blueprint_information, url_prefix="/information",
                       name="information")
app.register_blueprint(confirmation,
                       url_prefix="/email_confirmation")
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(blueprint_profile, name="profile")
app.register_blueprint(blueprint_register, name="register")
app.register_blueprint(blueprint_login, name="login")
app.register_blueprint(blueprint_cart, name="cart")
app.register_blueprint(blueprint_cart_add, name="cart_add")
app.register_blueprint(blueprint_cart_delete, name="cart_delete")
app.register_blueprint(blueprint_booking, name="booking")
app.register_blueprint(cloud, url_prefix='/cloud')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    session.get("id_user", 0)
    if request.method == "GET":
        db_session.global_init("db/users_data.db")
        db_sess = db_session.create_session()

        recommendations_list = []
        for book in db_sess.query(Books).filter(Books.rating > 0.9):
            recommendations_list.append((
                book.content, book.image, f'book/{book.id}'))

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
            primary_school_list.append((
                book.content, book.image, f'book/{book.id}'))

        secondary_school_list = []
        for book in db_sess.query(Books).filter((Books.limitation ==
                                                 "Средняя школа") |
                                                (Books.limitation.in_(
                                                    numbers_list[4:8])))[:3]:
            secondary_school_list.append((
                book.content, book.image, f'book/{book.id}'))

        high_school_list = []
        for book in db_sess.query(Books).filter((Books.limitation ==
                                                 "Старшая школа") |
                                                (Books.limitation.in_(
                                                    numbers_list[9:10])))[:3]:
            high_school_list.append((
                book.content, book.image, f'book/{book.id}'))

        students_list = []
        for book in db_sess.query(Books).filter((Books.limitation ==
                                                 "Студентам") |
                                                (Books.limitation ==
                                                 (numbers_list[-1])))[:3]:
            students_list.append((book.content, book.image, f'book/{book.id}'))

        return render_template("index.html",
                               title="book.akurmaev.ru",
                               recommendations_list=recommendations_list,
                               novelties_list=novelties_list,
                               primary_school_list=primary_school_list,
                               secondary_school_list=secondary_school_list,
                               high_school_list=high_school_list,
                               students_list=students_list)
    elif request.method == "POST":
        if request.form["button_search"] == "active":
            if request.form["search"]:
                return redirect(
                    f'/search/{request.form["search"].replace(" ", "%")}')
        return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
