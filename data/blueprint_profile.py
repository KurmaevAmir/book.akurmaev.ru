from flask import Blueprint, render_template, redirect
from data import db_session
from flask_login import login_required

blueprint_profile = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint_profile.route('/profile')
@login_required
def profile():
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    return render_template("profile.html")