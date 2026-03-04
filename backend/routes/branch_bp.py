from flask import Blueprint
from flask_restful import Api
from resources.branch import BranchListResource

branch_bp = Blueprint("branch_bp", __name__)
api = Api(branch_bp)

api.add_resource(BranchListResource, "/branches")
