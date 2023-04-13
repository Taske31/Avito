import flask
from flask import jsonify, make_response, request, render_template, redirect
from data import db_session
from data.announcements import Announcement
from forms import announcement_forms
from werkzeug.utils import secure_filename
import os

blueprint = flask.Blueprint(
    'announcement',
    __name__,
    template_folder='templates'
)


@blueprint.route('/make_announcement', methods=['GET', 'POST'])
def make_announcement():
    form = announcement_forms.AnnouncementForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            state=form.state.data,
            address=form.address.data,
            picture=form.pictures.data.filename
        )
        picture = form.pictures.data
        filename = secure_filename(picture.filename)
        picture.save(os.path.join('static/images', filename))
        db_sess.add(announcement)
        db_sess.commit()
        return redirect(f'/{announcement.id}')
    return render_template('announcement-make.html', title='Разместить объявление', form=form)


@blueprint.route('/<int:id>')
def announcement_view(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(Announcement).filter(Announcement.id == id).first()
    pictures = f'/static/images/{announcement.picture}'
    return render_template('announcement-view.html', announcement=announcement, pictures=pictures)
