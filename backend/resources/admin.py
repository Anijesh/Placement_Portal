from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models import Student, Company, Job
from extensions import db

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

class AdminCompanyListResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"message": "Admin access required"}, 403

        companies = Company.query.all()
        result = []
        for c in companies:
            result.append({
                "id": c.id,
                "name": c.name,
                "industry": c.industry,
                "location": c.location,
                "status": c.approval_status
            })
        return result, 200

class AdminCompanyApproveResource(Resource):
    @jwt_required()
    def put(self, id):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"message": "Admin access required"}, 403

        company = Company.query.get(id)
        if not company:
            return {"message": "Company not found"}, 404

        company.approval_status = "approved"
        db.session.commit()
        return {"message": "Company approved"}, 200

class AdminCompanyRejectResource(Resource):
    @jwt_required()
    def put(self, id):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"message": "Admin access required"}, 403

        company = Company.query.get(id)
        if not company:
            return {"message": "Company not found"}, 404

        company.approval_status = "rejected"
        db.session.commit()
        return {"message": "Company rejected"}, 200
    
class AdminStudentListResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"message": "Admin access required"}, 403
        students = Student.query.all()
        result =[]
        for student in students:
            result.append({
                "id":student.id,
                'name': student.name,
                'branch':student.branch.name,
                'email':student.user.email,
                'cgpa':student.cgpa,
                'graduation_year':student.graduation_year,
                'skills':student.skills
            })
        return result, 200
