from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from models import User, Student, Company, Job,Application
from extensions import db
from datetime import datetime


class CompanyCreateJob(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims.get("role") != 'company':
            return {"message": "Company access required"}
        data = request.get_json()
        deadline_date = datetime.strptime(data["deadline"], "%Y-%m-%d").date()
        company= Company.query.filter_by(user_id =get_jwt_identity()).first()
        job = Job(
            company_id=company.id,
            title=data["title"],
            description=data["description"],
            min_cgpa=data["min_cgpa"], 
            salary=data["salary"],
            deadline=deadline_date,
            status="pending"
        )

        db.session.add(job)
        db.session.commit()

        return {"message": "Placement drive created"}, 201

class CompanyJobList(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != 'company':
            return { "message":"Company access required"}
        company = Company.query.filter_by(user_id = get_jwt_identity()).first()
        jobs = Job.query.filter_by(company_id = company.id).all()
        results =[]
        for job in jobs:
            results.append({
                "id":job.id,
                "title" :job.title,
                "description" : job.description,
                "min_cgpa" : job.min_cgpa,
                "deadline" : str(job.deadline),
                "salary" : job.salary,
                "status" : job.status,
            })
        return results,200
    
class CompanyApplicatonList(Resource):
    @jwt_required()
    def get(self,id):
        claims = get_jwt()
        if claims.get('role') != 'company':
            return {"message":"company access required"},403
        company=Company.query.filter_by(user_id = get_jwt_identity()).first()
        job=Job.query.get(id)
        if(job.company != company):
            return {'message':"not access to see"},403
        applications=Application.query.filter_by(job_id= job.id).all()
        result=[]
        for application in applications:
            result.append({'application_id':application.id,
                           "job_title":application.job.title,
                           'student':application.student.name,
                           'branch':application.student.branch.name,
                           'cgpa':application.student.cgpa,
                           'skills':application.student.skills,
                           'graduation_year':str(application.student.graduation_year),
                           "status":application.status,
                           'salary':application.job.salary,
                           'applied_at':str(application.applied_at),

            })
        return result,200
class CompanyShortlistApplication(Resource):
    @jwt_required()
    def put(self,id):
        claims = get_jwt()
        if claims.get('role') != 'company':
            return {"message":"company access required"},403
        company=Company.query.filter_by(user_id = get_jwt_identity()).first()
        application = Application.query.get(id)
        if not application:
            return {'message':"Application not found"},404
        application.status='shortlisted'
        db.session.commit()
        return {"message": "Student shortlisted"}, 200