import flask
from flask import render_template, redirect, request
from flask_login import current_user, login_required
from data import db_session
from data.users import User
from data.books import Books

blueprint_information = flask.Blueprint(
    'add_book', __name__,
    static_folder="static",
    template_folder='templates'
)


@blueprint_information.route("/", methods=["GET", "POST"])
@login_required
def info():
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.booking != '').all()
    a = []

    if current_user.rights in ['Admin', 'Librarian']:
        if request.method == "POST":
            if request.form["button_search"] == "active":
                if request.form["search"]:
                    return redirect(f'/search/{request.form["search"].replace(" ", "%")}')
        books_id = []
        for i in user:
            book_title = []
            book_id = []

            for j in i.booking.split(', '):
                print(j)
                book = db_sess.query(Books).filter(Books.title == j).first()
                book_title.append(book.title)
                book_id.append(book.id)
                print(book_title)
                print(book_id)

            a.append([i.name, i.booking, i.id, book_title])
            books_id.append(book_id)
        print(books_id)
        print(a)
        return render_template("information.html", array=a, book_id=books_id)


@blueprint_information.route("/user_delete/<int:id>/<int:user_id>")
@login_required
def info_delete(id, user_id):
    print(1)
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    book = db_sess.query(Books).filter(Books.id == id).first()
    if book.status == '':
        book.status = '1'
    else:
        book.status = str(int(book.status) + 1)

    if ', ' in user.booking:
        book_len = len(book.title)

        if user.booking[:book_len] == book.title:
            user.booking = user.booking.replace(f'{book.title}, ', '')
        else:
            user.booking = user.booking.replace(f', {book.title}', '')
    else:
        user.booking = user.booking.replace(book.title, '')
    db_sess.commit()
    return redirect('/information')
