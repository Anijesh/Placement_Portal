from flask import Blueprint
from flask_restful import Api
from resources.student import(
    StudentJobList,
)

student_bp=Blueprint("student_bp",__name__)
api = Api(student_bp)

api.add_resource(StudentJobList,'/jobs/list')