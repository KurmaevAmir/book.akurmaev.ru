from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required
from data.users import User
from data.books import Books
from data import db_session

blueprint_cart = Blueprint("first_book", __name__,
                           static_folder="static",
                           template_folder="templates")


@blueprint_cart.route('/cart', methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if request.form["button_search"] == "active":
            if request.form["search"]:
                return redirect(
                    f'/search/{request.form["search"].replace(" ", "%")}')
    array = []
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == current_user.name).first()
    if ", " in user.shopping_cart:
        for i in user.shopping_cart.split(", "):
            book = db_sess.query(Books).filter(Books.title == i).first()
            array.append([book.title, book.image, book.id])
    elif user.shopping_cart:
        book = db_sess.query(Books).filter(
            Books.title == user.shopping_cart).first()
        array.append([book.title, book.image, book.id])
    return render_template("cart.html", array=array)
