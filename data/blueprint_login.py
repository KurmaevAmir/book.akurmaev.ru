from flask import Blueprint, render_template, redirect, session
from data import db_session
from data.users import User
from data.login import LoginForm
from flask_login import login_user, login_required, logout_user

blueprint_login = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint_login.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init("db/users_data.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            id_user = user.id
            session["id_user"] = id_user
            return redirect("/profile")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@blueprint_login.route('/logout')
@login_required
def logout():
    session["id_user"] = 0
    logout_user()
    return redirect("/")
