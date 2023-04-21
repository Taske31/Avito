from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField
from data import db_session, category


class AnnouncementForm(FlaskForm):
    category = SelectField('Категория', choices=[i.name for i in db_session.create_session().query(category.Category).all()], validators=[DataRequired()])
    title = StringField('Заголовок', validators=[DataRequired()])
    pictures = FileField('Приложите фотографии', validators=[FileRequired()])
    content = TextAreaField("Описание", validators=[DataRequired()])
    state = SelectField('Состояние', choices=['Б/У', 'Новое'], validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Разместить')
