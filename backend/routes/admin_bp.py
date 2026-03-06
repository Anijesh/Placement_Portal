from flask import Blueprint
from flask_restful import Api
from resources.admin import (
    AdminStatsResource,
    AdminCompanyListResource,
    AdminCompanyApproveResource,
    AdminCompanyRejectResource
)

admin_bp = Blueprint("admin_bp", __name__)
api = Api(admin_bp)

api.add_resource(AdminStatsResource, "/stats")
api.add_resource(AdminCompanyListResource, "/companies")
api.add_resource(AdminCompanyApproveResource, "/companies/<int:id>/approve")
api.add_resource(AdminCompanyRejectResource, "/companies/<int:id>/reject")
