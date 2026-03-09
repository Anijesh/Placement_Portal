from flask import Blueprint
from flask_restful import Api
from resources.company import(
    CompanyCreateJob,
)

company_bp=Blueprint('company_bp',__name__)
api=Api(company_bp)

api.add_resource(CompanyCreateJob,'/create/job')