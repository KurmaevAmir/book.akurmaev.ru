from flask import Blueprint, render_template

blueprint = Blueprint("first_book", __name__,
                      static_folder="static", template_folder="templates")


@blueprint.route('/pussinboots')
def index(title, img_src, book_title, description, cost):
    return render_template("first_book.html", title=title, img_src=img_src, book_title=book_title,
                           description=description, cost=cost)
