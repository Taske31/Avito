import flask
from flask import jsonify, make_response, request, render_template
from flask_login import current_user
from main import login_manager
blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates'
)


@blueprint.route('/')
def main_window():
    return render_template('main_window.html', current_user=current_user)
