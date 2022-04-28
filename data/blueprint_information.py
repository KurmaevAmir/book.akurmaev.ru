import flask
from flask import render_template
from flask_login import current_user, login_required
from data import db_session
from data.users import User

blueprint_information = flask.Blueprint(
    'add_book', __name__,
    static_folder="static",
    template_folder='templates'
)


@blueprint_information.route("/")
@login_required
def info():
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.booking is not None).all()
    a = []
    if current_user.rights in ['Admin', 'Librarian']:
        for i in user:
            a.append([i.name, i.booking])
        return render_template("information.html", array=a)
