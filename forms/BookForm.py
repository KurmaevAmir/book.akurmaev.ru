from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField("Название произведения",
                        validators=[DataRequired()])
    author = StringField("Автор произведения")
    content = StringField("Описание произведения")
    image = FileField("Обложка произведения",
                      validators=[DataRequired()])
    status = StringField("Наличие книги (укажите кол-во)",
                         validators=[DataRequired()])
    limitation = RadioField("Возрастное ограничение",
                            choices=["Начальная школа",
                                     "Средняя школа",
                                     "Старшая школа",
                                     "Студентам"])
    publishing_house = StringField("Издательство", validators=[DataRequired()])
    year_publishing = StringField("Год издания", validators=[DataRequired()])
    number_of_pages = IntegerField("Количество страниц", validators=[DataRequired()])
    submit = SubmitField("Применить")
