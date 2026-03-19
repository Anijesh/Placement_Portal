from flask import Blueprint
from flask_restful import Api
from resources.auth import RegisterResource, LoginResource, LogoutResource

auth_bp = Blueprint("auth_bp", __name__)
api = Api(auth_bp)

api.add_resource(RegisterResource, "/register")
api.add_resource(LoginResource, "/login")
api.add_resource(LogoutResource, "/logout")