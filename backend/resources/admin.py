from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models import Student, Company, Job,User ,Application,Placement
from extensions import db, cache

class AdminStatsResource(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return {"message": "Admin access required"}, 403

        students = Student.query.count()
        companies = Company.query.count()
        jobs = Job.query.count()
        applications = Application.query.count()
        return {
            "students": students,
            "companies": companies,
            "jobs": jobs,
            "applications": applications
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
                "website": c.website,
                "hr_contact": c.hr_contact,
                "status": c.approval_status,
                "is_active": c.user.is_active
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
        cache.clear()
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
        cache.clear()
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
                'skills':student.skills,
                'is_active': student.user.is_active
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
        cache.clear()
        return {"message": "Student deactivated"}, 200
    
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
        cache.clear()
        return{"message":"Company deactivated"}, 200
    
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
        cache.clear()
        return {"message": "Student activated"},200
    
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
        cache.clear()
        return{"message":"Company activated"},200
    

class AdminSearchStudents(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        claims = get_jwt()
        if claims.get('role') !='admin':
            return {"message":"Admin access required"},403      
        query= request.args.get('q')
        
        try:
            query_id = int(query)
            students = Student.query.join(User).filter(
                (Student.id == query_id) |
                (Student.name.ilike(f"%{query}%")) |
                (Student.skills.ilike(f"%{query}%")) |
                (User.email.ilike(f"%{query}%"))
            ).all()
        except (ValueError, TypeError):
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
    
class AdminSearchCompanies(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        claims=get_jwt()
        if claims.get('role') != 'admin':
            return {"message":"Admin access required"},403
        query= request.args.get('q')
        companies = Company.query.filter(
            (Company.name.ilike(f"%{query}%")) |
            (Company.industry.ilike(f"%{query}%")) |
            (Company.location.ilike(f"%{query}%"))
        ).all()

        result = []

        for c in companies:
            result.append({
                "id": c.id,
                "name": c.name,
                "industry": c.industry,
                "location": c.location,
                "website": c.website,
                "hr_contact": c.hr_contact,
                "status": c.approval_status,
                "is_active": c.user.is_active
            })
        return result, 200
    

class AdminJobList(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self):
        claims=get_jwt()
        if claims.get('role') != 'admin':
            return{"message":"admin access required"},403
        jobs =Job.query.all()
        result =[]
        for job in jobs:
            result.append({
                "id":job.id,
                "company":job.company.name,
                "title" :job.title,
                "description" : job.description,
                "min_cgpa" : job.min_cgpa,
                "deadline" : str(job.deadline),
                "salary" : job.salary,
                "status" : job.status,
            })
        return result,200
    
class AdminJobApprove(Resource):
    @jwt_required()
    def put(self,id):
        claims=get_jwt()
        if claims.get('role') != 'admin':
            return {"message":"admin access required"},403
        job = Job.query.get(id)
        if not job:
            return{"message": "job not found"},404
        job.status="approved"
        db.session.commit()
        cache.clear()
        return {"message": "Placement drive approved"}, 200
        

class AdminJobReject(Resource):
    @jwt_required()
    def put(self,id):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {"message": "admin access required"},403
        job = Job.query.get(id)
        if not job:
            return{"message": 'job not found'},404   
        job.status ='rejected'
        db.session.commit()
        cache.clear()
        return{'message':"placement drive rejected"},200


class AdminApplicationList(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {'message': 'admin access required'}, 403

        applications= Application.query.all()
        result=[]
        for application in applications:
            result.append({
                'application_id':application.id,
                'student_name':application.student.name,
                'student_branch':application.student.branch.name,
                'company':application.job.company.name,
                'job_title':application.job.title,
                'offered_salary':application.job.salary,
                'status':application.status,
            })
        return result,200
        
class AdminPlacementList(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {"message": "admin access required"},403
        placements=Placement.query.all()
        result =[]
        for placement in placements:
            result.append({
                'application_id':placement.application.id,
                'student_name':placement.application.student.name,
                'company_name':placement.application.job.company.name,
                'job_title': placement.application.job.title,
                'offered_salary':placement.offered_salary,
                'joining_date':str(placement.joining_date),
            })
        return result,200

