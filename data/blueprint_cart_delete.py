from flask import Blueprint, redirect
from flask_login import current_user, login_required
from data.books import Books
from data import db_session

blueprint_cart_delete = Blueprint("first_book", __name__,
                                  static_folder="static",
                                  template_folder="templates")


@blueprint_cart_delete .route('/cart_delete/<int:id>')
@login_required
def index(id):
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == id).first()
    if book.status == '':
        book.status = '1'
    else:
        book.status = str(int(book.status) + 1)
    if ', ' in current_user.shopping_cart:
        book_len = len(book.title)
        if current_user.shopping_cart[:book_len] == book.title:
            current_user.shopping_cart = \
                current_user.shopping_cart.replace(f'{book.title}, ', '')
        else:
            current_user.shopping_cart = \
                current_user.shopping_cart.replace(f', {book.title}', '')
    else:
        current_user.shopping_cart = \
            current_user.shopping_cart.replace(book.title, '')
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect("/cart")
