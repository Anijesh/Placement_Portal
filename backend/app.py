from flask import Flask
from config import Config
from extensions import db, jwt, cors
from routes.auth_bp import auth_bp
from routes.branch_bp import branch_bp
from routes.admin_bp import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(branch_bp, url_prefix="/api")
    app.register_blueprint(admin_bp,url_prefix="/api/admin")

    return app