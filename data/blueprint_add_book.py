import os
import random

import flask
from flask import render_template, session
from flask_login import current_user
from werkzeug.exceptions import abort
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


symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
           "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
           "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
           "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
           "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
           "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
           "Y", "Z", "-", "_"]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generationFilename(filename_used):
    filename = ""
    for i in range(38):
        filename += random.choice(symbols)
    while filename in filename_used:
        filename = generationFilename()
    return filename


@add_book.route("/", methods=["GET", "POST"])
def adding():
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id ==
                                      session["id_user"]).first()
    try:
        if user.rights == "Admin":
            form = BookForm()
            if form.validate_on_submit():
                if form.image.data and \
                        allowed_file(form.image.data.filename):
                    filename_used = db_sess.query(Books.image).all()
                    filename_used = [i[0] for i in filename_used]
                    extension = form.image.data.filename.split(".")[-1]
                    filename = generationFilename(filename_used)
                    filename = filename + f".{extension}"
                    file_path = os.path.join(current_app.config
                                             ['UPLOAD_FOLDER'],
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
    except:
        abort(404)
