from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.data_to_save import ALLOWED_EXTENSIONS, UPLOAD_FOLDER_AVATAR
import os

blueprint_profile = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint_profile.route('/profile', methods=['GET', 'POST'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint_profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "POST":
        if request.form['search'] and request.method == "POST":
            text = request.form['search'].replace(" ", '%')
            return redirect(f'/search/{text}')
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if request.method == 'GET':
        return render_template("profile.html", avatar_url=user.avatar)
    elif request.method == 'POST':
        f = 0
        last = 0
        if 'file' in request.files:
            f = request.files['file']

            if allowed_file(f.filename):
                extension = f.filename.split(".")[-1]
                filename = f'{user.id}.{extension}'
                f.save(os.path.join(UPLOAD_FOLDER_AVATAR, filename))
                user.avatar = f'/static/avatars/{filename}'
                db_sess.commit()

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
        return render_template('profile.html', avatar_url=user.avatar)


