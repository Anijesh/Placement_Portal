from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from models import Student, Company, Job,User,Application
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
    
class StudentApplyJob(Resource):
    @jwt_required()
    def post(self,id):
        claims = get_jwt()
        if claims.get('role') != 'student':
            return {"message":"Student access required"},403
        job = Job.query.get(id)
        if not job:
            return {"message": "Job not found"}, 404
        if job.status != 'approved':
            return {'message':"This drive is not in active status"},400
        student = Student.query.filter_by(user_id=get_jwt_identity()).first()
        existing = Application.query.filter_by(student_id=student.id,job_id=job.id).first()
        if existing:
            return {'message':"Already applied for Application"},400
        application=Application(student_id = student.id,
                                job_id = job.id)
        db.session.add(application)
        db.session.commit()
        return {"message":"Application submitted successfully"},201
        