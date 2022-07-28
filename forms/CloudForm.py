from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CloudForm(FlaskForm):
    title = StringField("Название произведения",
                        validators=[DataRequired()])
    link = StringField("Ссылка на электронную версию",
                       validators=[DataRequired()])
    submit = SubmitField("Применить")
