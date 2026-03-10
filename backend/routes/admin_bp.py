from flask import Blueprint
from flask_restful import Api
from resources.admin import (
    AdminStatsResource,
    AdminCompanyListResource,
    AdminCompanyApproveResource,
    AdminCompanyRejectResource,
    AdminStudentListResource,
    AdminDeactivateStudent,
    AdminDeactivateCompany,
    AdminActivateStudent,
    AdminActivateCompany,
    AdminSearchStudents,
    AdminSearchCompanies,
    AdminJobList,
)

admin_bp = Blueprint("admin_bp", __name__)
api = Api(admin_bp)

api.add_resource(AdminStatsResource, "/stats")
api.add_resource(AdminCompanyListResource, "/companies")
api.add_resource(AdminCompanyApproveResource, "/companies/<int:id>/approve")
api.add_resource(AdminCompanyRejectResource, "/companies/<int:id>/reject")
api.add_resource(AdminStudentListResource,'/students')
api.add_resource(AdminDeactivateStudent,'/students/<int:id>/deactivate')
api.add_resource(AdminDeactivateCompany,'/companies/<int:id>/deactivate')
api.add_resource(AdminActivateStudent,'/students/<int:id>/activate')
api.add_resource(AdminActivateCompany,'/companies/<int:id>/activate')
api.add_resource(AdminSearchStudents,'/students/search')
api.add_resource(AdminSearchCompanies,'/companies/search')
api.add_resource(AdminJobList,'/job/list')
