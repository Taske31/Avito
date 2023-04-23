import flask
from flask import render_template, redirect, abort, request
from data import db_session
from data.announcements import Announcement
from forms import announcement_forms
from werkzeug.utils import secure_filename
import os
from flask_login import current_user, login_required

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
        announcement = Announcement()
        announcement.title = form.title.data
        announcement.content = form.content.data
        announcement.state = form.state.data
        announcement.address = form.address.data
        announcement.picture = form.pictures.data.filename
        picture = form.pictures.data
        announcement.category = form.category.data
        filename = secure_filename(picture.filename)
        picture.save(os.path.join('static/images', filename))
        current_user.announcements.append(announcement)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('announcement-make.html', title='Разместить объявление', form=form)


@blueprint.route('/<int:id>')
@login_required
def announcement_view(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(Announcement).filter(Announcement.id == id).first()
    pictures = f'/static/images/{announcement.picture}'
    in_following = announcement.id in [i.id for i in current_user.following]
    personal_ann = announcement.id in [i.id for i in current_user.announcements]
    return render_template('announcement-view.html', announcement=announcement, pictures=pictures,
                           in_following=in_following, personal_ann=personal_ann)


@blueprint.route('/announcement-delete/<int:id>', methods=['GET', 'POST'])
@login_required
def announcement_delete(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(Announcement).filter(Announcement.id == id).first()
    if announcement:
        db_sess.delete(announcement)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/personal-area-main')


@blueprint.route('/announcement-edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    form = announcement_forms.AnnouncementForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        announcement = db_sess.query(Announcement).filter(Announcement.id == id,
                                          Announcement.user == current_user
                                          ).first()
        if announcement:
            form.title.data = announcement.title
            form.content.data = announcement.content
            form.address.data = announcement.address
            form.state.data = announcement.state
            os.remove(f'static/images/{announcement.picture}')
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        announcement = db_sess.query(Announcement).filter(Announcement.id == id,
                                          Announcement.user == current_user
                                          ).first()
        if announcement:
            announcement.title = form.title.data
            announcement.content = form.content.data
            announcement.state = form.state.data
            announcement.address = form.address.data
            announcement.picture = form.pictures.data.filename
            picture = form.pictures.data
            filename = secure_filename(picture.filename)
            picture.save(os.path.join(f'static/images/', filename))
            db_sess.commit()
            return redirect('/personal-area-main')
        else:
            abort(404)
    return render_template('/announcement-make.html',
                           title='Редактирование объявление',
                           form=form
                           )


@blueprint.route('/following/<int:id>', methods=['GET', 'POST'])
@login_required
def following(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(Announcement).filter(Announcement.id == id).first()
    current_db_sessions = db_sess.object_session(announcement)
    current_db_sessions.close()
    if announcement and announcement.id not in [i.id for i in current_user.following]:
        current_user.following.append(announcement)
        db_sess.merge(current_user)
        db_sess.commit()
    return redirect(f'/{id}')


@blueprint.route('/following-delete/<int:id>', methods=['GET', 'POST'])
@login_required
def following_delete(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(Announcement).filter(Announcement.id == id).first()
    current_db_sessions = db_sess.object_session(announcement)
    current_db_sessions.close()
    if announcement and announcement.id in [i.id for i in current_user.following]:
        current_user.following.remove(current_user.following[[i.id for i in current_user.following].index(announcement.id)])
        db_sess.merge(current_user)
        db_sess.commit()
    return redirect(f'/{id}')
