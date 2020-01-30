from extensions import jwt
from auth.auth import auth_blueprint
from informer.events import events_blueprint
from flask import Flask
import connection
import mongoengine

def create_app():
    app = Flask(__name__)

    app.secret_key = 'secret'

    jwt.init_app(app)

    mongoengine.connect(db = connection.DB_NAME, username = connection.DB_USER, password = connection.DB_PASS, host = connection.DB_HOST, port = 27017)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(events_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()