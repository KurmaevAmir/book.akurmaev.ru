from flask import Blueprint, render_template
from werkzeug.utils import redirect

from data.email_confirmation import EmailConfirmation

confirmation = Blueprint("confirmation", __name__,
                         static_folder="static",
                         template_folder="templates")


@confirmation.route("/", methods=["GET", "POST"])
def email_confirmation():
    form = EmailConfirmation()
    confirmation_code = ""
    if form.validate_on_submit():
        if form.confirmation_code != confirmation_code:
            return render_template("email.confirmation.html",
                                   form=form,
                                   message="Неправильно указанный "
                                           "код подтверждения")
        return redirect("/login")
    return render_template("email.confirmation.html",
                           title="Подтверждение почты",
                           form=form)
