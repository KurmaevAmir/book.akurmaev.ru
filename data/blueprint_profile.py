from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, logout_user, current_user
from data import db_session
from data.users import User
from werkzeug.utils import secure_filename
import os

blueprint_profile = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint_profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if request.method == 'GET':
        return render_template("profile.html")
    elif request.method == 'POST':
        f = 0
        last = 0
        if 'file' in request.files:
            f = request.files['file']

            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join('static/avatars/', filename))

        if request.form['last']:
            last = request.form['last']
            new = request.form['new']
            new_again = request.form['new_again']

            if user.check_password(last):

                if new == new_again:
                    user.set_password(new)
                    db_sess.commit()
                    logout_user()
                    return redirect('../')
                else:
                    return render_template("profile.html", message='Пароли не совпадают')
            else:
                return render_template("profile.html",
                                       message='Пароль не верный')
        return render_template('profile.html')


