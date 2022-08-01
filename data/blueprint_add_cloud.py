import flask
from flask import session, redirect, request, render_template, abort
from flask_login import current_user

from data import db_session
from data.electronic_version import ElectronicVersion
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
                electronic_version = ElectronicVersion()
                title_electronic_version = []
                for book in db_sess.query(ElectronicVersion).all():
                    title_electronic_version.append(book.title)
                if form.title.data in title_electronic_version:
                    print(1)
                    count = 1
                    title = form.title.data + f"({count})"
                    while title in title_electronic_version:
                        print(2)
                        count += 1
                        title = title.replace(f'{count - 1}', f'{count}')
                    electronic_version.title = title
                else:
                    electronic_version.title = form.title.data
                electronic_version.author = form.author.data
                electronic_version.link = form.link.data
                current_user.electronic_version.append(electronic_version)
                db_sess.merge(current_user)
                db_sess.commit()
                return redirect("/")
            if request.method == "POST":
                if request.form["button_search"] == "active":
                    if request.form['search']:
                        return redirect(
                            f'/search'
                            f'{request.form["search"].replace(" ", "%")}'
                        )
            return render_template("add_cloud.html",
                                   title="Добавление электронной версии",
                                   form=form)
        else:
            abort(404)
    except:
        abort(404)
