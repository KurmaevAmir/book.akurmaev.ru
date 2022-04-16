from flask import Blueprint, render_template

from data import db_session
from data.books import Books

search = Blueprint("search", __name__,
                   static_folder="static",
                   template_folder="templates")


@search.route("/<keys>", methods=["GET"])
def searching(keys):
    title = keys.replace("%", " ")
    keys = keys.replace("%", "% %")
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    output_list = []
    for book in db_sess.query(Books).filter(
            (Books.title.like(keys))
    ):
        output_list.append((book.id, book.title, book.content))
    if not bool(output_list):
        return render_template("search.html", title=title, status=False)
    len_output = len(output_list)
    return render_template("search.html", title=title, status=True,
                           keys=title, output_list=output_list)
