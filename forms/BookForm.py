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
    status = IntegerField("Наличие книги (укажите кол-во)",
                          validators=[DataRequired()])
    limitation = RadioField("Возрастное ограничение",
                            choices=["Начальная школа",
                                     "Средняя школа",
                                     "Старшая школа",
                                     "Студентам"])
    submit = SubmitField("Применить")
