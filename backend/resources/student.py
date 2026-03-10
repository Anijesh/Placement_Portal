from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models import Student, Company, Job,User
from extensions import db

class StudentJobList(Resource):
    @jwt_required()
    def get(self):
        claims=get_jwt()
        if claims.get('role') != 'student':
            return {"message":"student access required"},403
        jobs=Job.query.filter_by(status='approved').all()
        result =[]
        if not jobs:
            return {"message":"No job found"}
        for job in jobs:
            result.append({
                "id":job.id,
                "company":job.company.name,
                "title" :job.title,
                "description" : job.description,
                "min_cgpa" : job.min_cgpa,
                "deadline" : str(job.deadline),
                "salary" : job.salary,
            })
        return result,200