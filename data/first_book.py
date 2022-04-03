from flask import Blueprint, render_template
from data import db_session
from data.books import Books

blueprint = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint.route('/<id>')
def index(id):
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    for book in db_sess.query(Books).filter(Books.id == id):
        title = book.title
        img_src = book.image
        description = book.content
    return render_template("first_book.html", title=title,
                           img_src=img_src,
                           description=description)
