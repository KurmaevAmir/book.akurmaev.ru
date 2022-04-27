from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EmailConfirmation(FlaskForm):
    confirmation_code = StringField("Код потдверждения: ",
                                    validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")
