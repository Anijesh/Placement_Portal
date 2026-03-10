from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from models import User, Student, Company, Job
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
        return results
