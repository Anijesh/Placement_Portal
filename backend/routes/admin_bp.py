from flask import Blueprint
from flask_restful import Api
from resources.admin import AdminStatsResource

admin_bp = Blueprint("admin_bp", __name__)
api = Api(admin_bp)

api.add_resource(AdminStatsResource, "/stats")
