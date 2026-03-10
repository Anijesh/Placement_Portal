from flask import Blueprint
from flask_restful import Api
from resources.company import(
    CompanyCreateJob,
    CompanyJobList,
)

company_bp=Blueprint('company_bp',__name__)
api=Api(company_bp)

api.add_resource(CompanyCreateJob,'/create/job')
api.add_resource(CompanyJobList,'/job/list')