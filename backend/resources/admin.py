from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models import Student, Company, Job

class AdminStatsResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"message": "Admin access required"}, 403

        students = Student.query.count()
        companies = Company.query.count()
        jobs = Job.query.count()
        return {
            "students": students,
            "companies": companies,
            "jobs": jobs
        }, 200