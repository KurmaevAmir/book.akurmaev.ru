from flask import Blueprint, render_template, jsonify, request

from data import db_session
from data.books import Books

books = Blueprint("first_book", __name__,
                  static_folder="static",
                  template_folder="templates")


@books.route('/<int:id>', methods=['POST', 'GET'])
def index(id):
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    book = db_sess.query(Books).get(id)
    # if request.method == "POST":

    if not book:
        return jsonify({'error': 'Not found'})
    return render_template("first_book.html", title=book.title,
                           img_src=book.image, book_id=book.id,
                           description=book.content)
