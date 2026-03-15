from flask import Blueprint
from flask_restful import Api
from resources.student import(
    StudentJobList,
    StudentApplyJob,
    StudentApplicationList,
    StudentPlacementHistory,
)

student_bp=Blueprint("student_bp",__name__)
api = Api(student_bp)

api.add_resource(StudentJobList,'/jobs/list')
api.add_resource(StudentApplyJob,'/job/<int:id>/apply')
api.add_resource(StudentApplicationList,'/application/list')
api.add_resource(StudentPlacementHistory,'/placements')