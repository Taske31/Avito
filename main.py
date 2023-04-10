from flask import Flask
from flask_restful import Api
from data import main_page, db_session, users, users_blueprints, announcements_blueprints
from flask_login import LoginManager, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)


def main():
    db_session.global_init("db/avito-db.db")
    app.register_blueprint(main_page.blueprint)
    app.register_blueprint(users_blueprints.blueprint)
    app.register_blueprint(announcements_blueprints.blueprint)
    app.run()


if __name__ == '__main__':
    main()
