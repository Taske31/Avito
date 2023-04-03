import flask
from flask import jsonify, make_response, request, render_template

blueprint = flask.Blueprint(
    'announcement',
    __name__,
    template_folder='templates'
)


@blueprint.route('/make_announcement')
def make_announcement():
    return render_template('announcement.html')