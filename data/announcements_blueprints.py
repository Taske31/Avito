import flask
from flask import jsonify, make_response, request, render_template
from data import db_session
from data.announcements import Announcement

blueprint = flask.Blueprint(
    'announcement',
    __name__,
    template_folder='templates'
)


@blueprint.route('/make_announcement')
def make_announcement():
    return render_template('announcement-make.html')


@blueprint.route('/<int:id>')
def announcement_view(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(Announcement).filter(Announcement.id == id).first()
    pictures = f'/static/images/{str(id)}.jpg'
    return render_template('announcement-view.html', announcement=announcement, pictures=pictures)
