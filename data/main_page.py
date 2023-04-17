import flask
from flask import jsonify, make_response, request, render_template
from data import db_session
from flask_login import current_user
from data.announcements import Announcement
blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates'
)


@blueprint.route('/')
def main_page():
    print(1)
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        announcements = db_sess.query(Announcement).filter(current_user.id != Announcement.user_id).all()
    else:
        announcements = db_sess.query(Announcement).all()
    return render_template('main_page.html', current_user=current_user, announcements=announcements)
