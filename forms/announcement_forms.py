from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField


class AnnouncementForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    pictures = FileField('Приложите фотографии', validators=[FileRequired()])
    content = TextAreaField("Описание", validators=[DataRequired()])
    state = SelectField('Состояние', choices=['Б/У', 'Новое'], validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Разместить')
