from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models import Student, Company, Job,User
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

class AdminDeactivateStudent(Resource):
    @jwt_required()
    def put(self,id):
        claims =get_jwt()
        if claims.get('role') != 'admin':
            return {"message": "Admin access required"}, 403
        student = Student.query.get(id)
        if not student:
            return {"message": "Student not found"}, 404
        user = User.query.get(student.user_id)
        user.is_active = False
        db.session.commit()
        return {"message": "Student deactivated"}
    
class AdminDeactivateCompany(Resource):
    @jwt_required()
    def put(self,id):
        claims = get_jwt()
        if claims.get('role') !='admin':
            return {"message":"Admin access required"},403
        company = Company.query.get(id)
        if not company:
            return {'message':"Company not found"},404
        user=User.query.get(company.user.id)
        user.is_active = False
        db.session.commit()
        return{"message":"Company deactivated"}
    
class AdminActivateStudent(Resource):
    @jwt_required()
    def put(self,id):
        claims =get_jwt()
        if claims.get('role') != 'admin':
            return {"message": "Admin access required"}, 403
        student = Student.query.get(id)
        if not student:
            return {"message": "Student not found"}, 404
        user = User.query.get(student.user_id)
        user.is_active =True
        db.session.commit()
        return {"message": "Student activated"}
    
class AdminActivateCompany(Resource):
    @jwt_required()
    def put(self,id):
        claims = get_jwt()
        if claims.get('role') !='admin':
            return {"message":"Admin access required"},403
        company = Company.query.get(id)
        if not company:
            return {'message':"Company not found"},404
        user=User.query.get(company.user.id)
        user.is_active = True
        db.session.commit()
        return{"message":"Company activated"}
    

class AdminSearchStudents(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') !='admin':
            return {"message":"Admin access required"},403      
        query= request.args.get('q')
        students=Student.query.join(User).filter(
            (Student.name.ilike(f"%{query}%")) |
            (Student.skills.ilike(f"%{query}%")) |
            (User.email.ilike(f"%{query}%"))
        ).all()
        result=[]
        for s in students:
            result.append({
                "id": s.id,
                "name": s.name,
                "email": s.user.email,
                "branch": s.branch.name,
                "cgpa": s.cgpa,
                "graduation_year":s.graduation_year,
                "skills":s.skills,
                "is_active": s.user.is_active
            })
        return result, 200