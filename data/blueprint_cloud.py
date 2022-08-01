import flask
from flask import render_template

from data import db_session
from data.electronic_version import ElectronicVersion

cloud = flask.Blueprint(
    'cloud', __name__,
    static_folder='static',
    template_folder='templates'
)


@cloud.route("/")
def cloud_storage():
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    books = db_sess.query(ElectronicVersion).all()
    links_list = []
    for book in books:
        links_list.append((book.link, book.title, book.author))
    return render_template('cloud.html', links_list=links_list)
