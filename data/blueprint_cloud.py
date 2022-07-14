import flask
from flask import render_template

cloud = flask.Blueprint(
    'cloud', __name__,
    static_folder='static',
    template_folder='templates'
)


@cloud.route("/")
def cloud_storage():
    links_list = ['https://disk.yandex.ru/i/0MdRmrzIu1i0zA']
    return render_template('cloud.html', links_list=links_list)
