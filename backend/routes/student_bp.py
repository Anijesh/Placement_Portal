from flask import Blueprint
from flask_restful import Api
from resources.student import(
    StudentProfile,
    StudentJobList,
    StudentApplyJob,
    StudentApplicationList,
    StudentPlacementHistory,
    StudentExportCSV,
    StudentDownloadCSV
)

student_bp=Blueprint("student_bp",__name__)
api = Api(student_bp)

api.add_resource(StudentProfile,'/profile')
api.add_resource(StudentJobList,'/jobs/list')
api.add_resource(StudentApplyJob,'/job/<int:id>/apply')
api.add_resource(StudentApplicationList,'/application/list')
api.add_resource(StudentPlacementHistory,'/placements')
api.add_resource(StudentExportCSV,'/export/csv')
api.add_resource(StudentDownloadCSV, '/download/<string:filename>')