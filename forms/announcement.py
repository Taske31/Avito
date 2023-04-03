from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, MultipleFileField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    pictures = MultipleFileField('Приложите фотографии', validators=[DataRequired()])
    content = TextAreaField("Описание")
    state = SelectField('Состояние', choices=['Б/У', 'Новое'], validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Применить')
