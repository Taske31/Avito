import flask
from flask import jsonify, make_response, request, render_template
from data import db_session
from data.category import Category
from flask_login import current_user
from data.announcements import Announcement
blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates'
)


@blueprint.route('/')
def main_page():
    db_sess = db_session.create_session()
    categories = [i.name for i in db_sess.query(Category).all()]
    if current_user.is_authenticated:
        announcements = db_sess.query(Announcement).filter(current_user.id != Announcement.user_id).all()
    else:
        announcements = db_sess.query(Announcement).all()
    db_sess.close()
    return render_template('main_page.html', current_user=current_user, announcements=announcements,
                           categories=categories)


@blueprint.route('/search/category/<get_category>')
def search_by_categories(get_category):
    db_sess = db_session.create_session()
    categories = [i.name for i in db_sess.query(Category).all()]
    if current_user.is_authenticated:
        announcements = db_sess.query(Announcement).filter(current_user.id != Announcement.user_id,
                                                           Announcement.category == get_category).all()
    else:
        announcements = db_sess.query(Announcement).filter(Announcement.category == get_category).all()
    db_sess.close()
    return render_template('search-by-category.html', current_user=current_user, announcements=announcements,
                           categories=categories)


@blueprint.route('/search', methods=['GET', 'POST'])
def search():
    db_sess = db_session.create_session()
    categories = [i.name for i in db_sess.query(Category).all()]
    announcements = db_sess.query(Announcement).filter(Announcement.title == request.form.get('search-place'))
    db_sess.close()
    return render_template('search.html', announcements=announcements, categories=categories)

