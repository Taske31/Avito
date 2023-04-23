import flask
from flask import jsonify, make_response, request, render_template, redirect, abort
from data import db_session, users
from forms import user_forms
from data.users import User
from flask_login import login_user, logout_user, login_required, current_user
from data.announcements import Announcement

blueprint = flask.Blueprint(
    'register',
    __name__,
    template_folder='templates'
)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = user_forms.RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.number == form.number.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            number=form.number.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = user_forms.LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/personal-area-main', methods=['GET'])
def personal_area():
    db_sess = db_session.create_session()
    personal_announcements = db_sess.query(Announcement).filter(current_user.id == Announcement.user_id).all()
    db_sess.close()
    return render_template('personal-area-main.html', personal_announcements=personal_announcements)


@blueprint.route('/personal-area-following', methods=['GET'])
def personal_area_following():
    db_sess = db_session.create_session()
    following_list = [i.id for i in current_user.following]
    following_announcements = db_sess.query(Announcement).filter(Announcement.id.in_(following_list)).all()
    db_sess.close()
    return render_template('personal-area-following.html', following_announcements=following_announcements)
