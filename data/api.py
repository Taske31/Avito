import flask
from data import db_session
from data.announcements import Announcement
from flask import jsonify, request


blueprint = flask.Blueprint(
    'announcements_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/announcements', methods=['GET'])
def get_announcements():
    db_sess = db_session.create_session()
    announcements = db_sess.query(Announcement).all()
    if not announcements:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'Announcements':
                [item.to_dict(only=('id', 'title', 'content', 'user.name', 'created_date', 'category', 'address', 'state'))
                 for item in announcements]
        }
    )


@blueprint.route('/api/announcements/<int:id>', methods=['GET'])
def get_one_announcements(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(Announcement).get(id)
    if not announcement:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'Announcement':
                announcement.to_dict(
                    only=('title', 'content', 'user.name', 'created_date', 'category', 'address', 'state'))

        }
    )


@blueprint.route('/api/announcements/<int:id>', methods=['DELETE'])
def delete_news(id):
    db_sess = db_session.create_session()
    announcements = db_sess.query(Announcement).get(id)
    if not announcements:
        return jsonify({'error': 'Not found'})
    db_sess.delete(announcements)
    db_sess.commit()
    return jsonify({'success': 'OK'})
