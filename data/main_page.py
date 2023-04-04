import flask
from flask import jsonify, make_response, request, render_template
from data import db_session
from flask_login import current_user
from data.announcements import Announcement
from main import login_manager
blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates'
)


@blueprint.route('/')
def main_window():
    db_sess = db_session.create_session()
    announcements = db_sess.query(Announcement).all()
    return render_template('main_window.html', current_user=current_user, announcements=announcements)
