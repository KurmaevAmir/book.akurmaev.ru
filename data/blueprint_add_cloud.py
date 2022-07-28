from os import abort

import flask
from flask import session

from data import db_session
from data.users import User
from forms.CloudForm import CloudForm

add_cloud = flask.Blueprint(
    'add_cloud', __name__,
    static_folder="static",
    template_folder="templates"
)


@add_cloud.route("/", methods=["GET", "POST"])
def adding_cloud():
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).filter(User.id ==
                                          session["id_user"]).first()
        if user.rights in ["Admin", "Librarian"]:
            form = CloudForm()
            if form.validate_on_submit():
                if form.title
        else:
            abort(404)
    except:
        abort(404)
