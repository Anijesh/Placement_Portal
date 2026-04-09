from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_caching import Cache

jwt=JWTManager()
cors=CORS()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()