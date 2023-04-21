from flask import Flask
from flask_restful import Api
from data import db_session, users
from flask_login import LoginManager, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = '994e790abda708fa1ae50f2d1fcdd90dc598a6df'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)


def main():
    db_session.global_init("db/avito-db.db")
    from data import main_page, users_blueprints, announcements_blueprints
    app.register_blueprint(main_page.blueprint)
    app.register_blueprint(users_blueprints.blueprint)
    app.register_blueprint(announcements_blueprints.blueprint)
    app.run()


if __name__ == '__main__':
    main()
