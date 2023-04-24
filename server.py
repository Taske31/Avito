from flask import Flask, make_response, jsonify
from flask_restful import Api
from data import db_session, users
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '994e790abda708fa1ae50f2d1fcdd90dc598a6df'  # Секретный ключ
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Обработка ошибок сервера
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(401)
def not_found(error):
    return make_response(jsonify({'error': 'unauthorized'}), 401)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 500)


# Загрузка пользователся
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)


# запуск приложения
def main():
    db_session.global_init("db/avito-db.db")
    from data import main_page, users_blueprints, announcements_blueprints, api
    app.register_blueprint(main_page.blueprint)
    app.register_blueprint(users_blueprints.blueprint)
    app.register_blueprint(announcements_blueprints.blueprint)
    app.register_blueprint(api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
