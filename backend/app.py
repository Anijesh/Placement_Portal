from flask import Flask
from config import Config
from extensions import db, jwt, cors
from routes.auth_bp import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app