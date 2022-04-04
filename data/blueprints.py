from flask import Blueprint, render_template, redirect
from data import db_session
from data.books import Books
from data.register import RegisterForm
import datetime
from data.users import User

blueprint = Blueprint("first_book", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint.route('/<int:id>')
def index(id):
    db_session.global_init("db/users_data.db")
    db_sess = db_session.create_session()
    for book in db_sess.query(Books).filter(Books.id == id):
        title = book.title
        img_src = book.image
        description = book.content
    return render_template("first_book.html", title=title,
                           img_src=img_src,
                           description=description)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if 1 > form.number.data > 11:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверный номер класса")
        if len(form.letter.data) > 1 or form.letter.data not in ['А', 'Б', 'В', 'Г']:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверная литера")
        db_session.global_init("db/users_data.db")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            hashed_password=form.password.data,
            created_date=datetime.datetime.now(),
            rights="User",
            parallel_number_student=form.number.data,
            letter=form.letter.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)