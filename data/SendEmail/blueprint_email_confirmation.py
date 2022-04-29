import random

from dotenv import load_dotenv
from flask import Blueprint, render_template, session, abort
from werkzeug.utils import redirect

from data import db_session
from data.SendEmail.mail_send import send_email
from data.users import User
from forms.email_confirmation import EmailConfirmation

load_dotenv()

confirmation = Blueprint("confirmation", __name__,
                         static_folder="static",
                         template_folder="templates")


def creating_confirmation_code(confirmation_code):
    if confirmation_code != "":
        for i in range(6):
            confirmation_code += str(random.randint(0, 9))
    return confirmation_code


@confirmation.route("/", methods=["GET", "POST"])
def email_confirmation():
    form = EmailConfirmation()
    try:
        data_session = session["login_data"]
    except:
        abort(404)
    confirmation_code = data_session[-1]
    send_email(data_session[1], "Подтверждение регистрации на сайте book.akurmaev.ru",
               confirmation_code)
    if form.validate_on_submit():
        if confirmation_code == form.confirmation_code.data:
            db_sess = db_session.create_session()
            user = User()
            user.name = data_session[0]
            user.parallel_number_student = data_session[3]
            user.letter = data_session[4]
            user.email = data_session[1]
            user.security_code = data_session[5]
            if data_session[3] == 837450:
                user.rights = 'Librarian'
                user.parallel_number_student = None
                user.letter = None

            user.set_password(data_session[2])

            db_sess.add(user)
            db_sess.commit()
            session.pop("login_data", None)
            return redirect("/login")
        return render_template("email_confirmation.html",
                               form=form,
                               message="Неправильно указан "
                                       "код подтверждения")
    return render_template("email_confirmation.html",
                           title="Подтверждение почты",
                           form=form)
