from flask import Blueprint, render_template, redirect, request
from data import db_session
from flask_login import login_required

blueprint_profile = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint_profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "POST":
        if request.form['search'] and request.method == "POST":
            text = request.form['search'].replace(" ", '%')
            return redirect(f'/search/{text}')
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    return render_template("profile.html")