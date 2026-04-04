from flask import Blueprint
from flask_restful import Api
from resources.company import(
    CompanyProfile,
    CompanyCreateJob,
    CompanyJobList,
    CompanyApplicatonList,
    CompanyShortlistApplication,
    CompanyRejectApplication,
    CompanyAcceptApplication,
    CompanyCloseJob,
    CompanyReopenJob,
    CompanyScheduleInterview,
)

company_bp=Blueprint('company_bp',__name__)
api=Api(company_bp)

api.add_resource(CompanyProfile,'/profile')
api.add_resource(CompanyCreateJob,'/create/job')
api.add_resource(CompanyJobList,'/job/list')
api.add_resource(CompanyApplicatonList,'/job/application/<int:id>/list')
api.add_resource(CompanyShortlistApplication,'/application/<int:id>/shortlist')
api.add_resource(CompanyRejectApplication,'/application/<int:id>/reject')
api.add_resource(CompanyAcceptApplication,'/application/<int:id>/accept')
api.add_resource(CompanyCloseJob,'/job/<int:id>/close')
api.add_resource(CompanyReopenJob,'/job/<int:id>/reopen')
api.add_resource(CompanyScheduleInterview,'/application/<int:id>/interview')