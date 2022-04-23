from flask import Blueprint, redirect
from flask_login import current_user, login_required
from data.books import Books
from data import db_session

blueprint_book_add = Blueprint("first_book", __name__,
                  static_folder="static",
                  template_folder="templates")


@blueprint_book_add .route('/book_add/<int:id>', methods=['GET', 'POST'])
@login_required
def index(id):
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == id).first()
    if current_user.shopping_cart:
        current_user.shopping_cart += f", {book.title}"
    else:
        current_user.shopping_cart += book.title
    db_sess.merge(current_user)
    db_sess.commit()
    print(current_user.name, current_user.shopping_cart)
    return redirect("../")