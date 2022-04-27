from flask import Blueprint, redirect
from flask_login import current_user, login_required
from data.users import User
from data import db_session

blueprint_booking = Blueprint("first_book", __name__,
                  static_folder="static",
                  template_folder="templates")


@blueprint_booking.route('/booking')
@login_required
def index():
    array = []
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.booking = user.shopping_cart
    user.shopping_cart = ''
    db_sess.commit()
    return redirect('../')
