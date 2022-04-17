from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from data import db_session
from data.books import Books

search = Blueprint("search", __name__,
                   static_folder="static",
                   template_folder="templates")


@search.route("/<keys>", methods=["GET", "POST"])
def searching(keys):
    if request.method == "GET":
        title = keys.replace("%", " ")
        keys = keys.replace("%", "% %")
        db_session.global_init("db/users_data.db")
        db_sess = db_session.create_session()
        output_list = []
        for book in db_sess.query(Books).filter(
                ((Books.title.like(keys)) |
                 (Books.author.like(keys)))
        ):
            output_list.append((book.id, book.title, book.image))
        if not bool(output_list):
            return render_template("search.html", title=title, status=False)
        len_output = len(output_list)
        return render_template("search.html", title=title, status=True,
                               keys=title, output_list=output_list,
                               len_output=len_output)
    elif request.method == "POST":
        text = request.form['search'].replace(' ', '%')
        return redirect(f"/search/{text}")
