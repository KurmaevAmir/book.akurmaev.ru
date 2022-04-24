import os

import flask
from flask import render_template
from flask_login import current_user
from werkzeug.utils import redirect, secure_filename
from flask import current_app

from data import db_session
from data.books import Books
from data.data_to_save import ALLOWED_EXTENSIONS
from data.users import User
from forms.BookForm import BookForm

add_book = flask.Blueprint(
    'add_book', __name__,
    static_folder="static",
    template_folder='templates'
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@add_book.route("/", methods=["GET", "POST"])
def adding():
    db_sess = db_session.create_session()
    db_session.global_init("db/users_data.db")
    form = BookForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                 filename)
        form.image.data.save(file_path)
        books = Books()
        books.title = form.title.data
        books.content = form.content.data
        books.author = form.author.data
        books.image = "/" + file_path
        if form.status.data < 0:
            books.status = "out"
        elif form.status.data == 0:
            books.status = "out"
        else:
            books.status = str(form.status.data)
        books.limitation = form.limitation.data
        current_user.books.append(books)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template("add_book.html",
                           title="Добавление книги",
                           form=form)
