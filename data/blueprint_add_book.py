import flask
from flask import render_template
from flask_login import current_user
from werkzeug.utils import redirect

from data import db_session
from data.books import Books
from forms.BookForm import BookForm

add_book = flask.Blueprint(
    'add_book', __name__,
    static_folder="static",
    template_folder='templates'
)


@add_book.route("/", methods=["GET", "POST"])
def adding():
    db_session.global_init("db/users_data.db")
    form = BookForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        books = Books()
        books.title = form.title.data
        books.content = form.content.data
        books.author = form.author.data
        books.image = form.image.data
        if form.status.data < 0:
            books.status = "out"
        elif form.status.data == 0:
            books.status = "out"
        else:
            books.status = str(form.status.data)
        books.limitation = form.limitation.data
        current_user.books.append(books)
        db_sess.merge(current_user)
        print(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template("add_book.html",
                           title="Добавление книги",
                           form=form)
