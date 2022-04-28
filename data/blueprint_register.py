import random

from flask import Blueprint, render_template, redirect, session
from data import db_session
from forms.register import RegisterForm
from data.users import User

blueprint_register = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint_register.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        if 1 > form.number.data or 11 < form.number.data:
            return render_template('register.html',
                                   form=form,
                                   message="Неверный номер класса")
        if len(form.letter.data) > 1 or form.letter.data not in ['А', 'Б', 'В', 'Г']:
            return render_template('register.html',
                                   form=form,
                                   message="Неверная литера")
        db_session.global_init("db/users_data.db")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        session.get('login_data', 0)
        confirmation_code = ""
        for i in range(6):
            confirmation_code += str(random.randint(0, 9))
        session["login_data"] = [form.name.data, form.email.data,
                                 form.password.data, form.number.data,
                                 form.letter.data, confirmation_code]
        return redirect('/email_confirmation')
    return render_template('register.html', form=form)
