from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, \
    EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    name = StringField('Фамилия Имя', validators=[DataRequired()])
    number = IntegerField('Класс', validators=[DataRequired()])
    letter = StringField('Литера', validators=[DataRequired()])
    submit = SubmitField('Подтвердить почту')
