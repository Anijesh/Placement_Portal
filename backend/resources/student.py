from flask import request, send_from_directory, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from models import Student, Company, Job,User,Application
from extensions import db, cache
import os

class StudentDownloadCSV(Resource):
    @jwt_required()
    def get(self, filename):
        claims = get_jwt()
        if claims.get('role') != 'student':
            return {"message": "Student access required"}, 403
            
        static_dir = 'static/exports'
        file_path = f"{static_dir}/{filename}"
        
        if not os.path.exists(file_path):
            return {"message": "File not found or still processing"}, 404
            
        return send_from_directory(static_dir, filename, as_attachment=True)

class StudentExportCSV(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != 'student':
            return {"message": "Student access required"}, 403
            
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        from tasks import export_applications_csv
        task = export_applications_csv.delay(user_id=user_id, role='student', email_to_notify=user.email)
        
        return {"message": "Export started. You will receive an email alert when it is complete.", "task_id": task.id}, 202

class StudentProfile(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != 'student':
            return {"message": "Student access required"}, 403
        student = Student.query.filter_by(user_id=get_jwt_identity()).first()
        if not student:
            return {"message": "Student not found"}, 404
        return {
            "id": student.id,
            "name": student.name,
            "branch_id": student.branch_id,
            "branch": student.branch.name if student.branch else None,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "skills": student.skills,
            "experience": student.experience,
            "resume_link": student.resume_link
        }, 200

    @jwt_required()
    def put(self):
        claims = get_jwt()
        if claims.get('role') != 'student':
            return {"message": "Student access required"}, 403
        student = Student.query.filter_by(user_id=get_jwt_identity()).first()
        if not student:
            return {"message": "Student not found"}, 404
        
        data = request.get_json()
        if 'name' in data:
            student.name = data['name']
        if 'branch_id' in data:
            student.branch_id = data['branch_id']
        if 'cgpa' in data:
            student.cgpa = float(data['cgpa']) if data['cgpa'] else None
        if 'graduation_year' in data:
            student.graduation_year = int(data['graduation_year']) if data['graduation_year'] else None
        if 'skills' in data:
            student.skills = data['skills']
        if 'experience' in data:
            student.experience = data['experience']
        if 'resume_link' in data:
            student.resume_link = data['resume_link']
            
        db.session.commit()
        cache.clear()
        return {"message": "Profile updated successfully"}, 200

class StudentJobList(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
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
                "eligible_branches": [b.name for b in job.eligible_branches],
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
        if student.cgpa < job.min_cgpa:
            return {"message": "You do not meet the CGPA requirement"}, 400
        branch_ids = [branch.id for branch in job.eligible_branches]
        if branch_ids and student.branch_id not in branch_ids:
            return {"message": "Your branch is not eligible for this drive"}, 400
        application=Application(student_id = student.id,
                                job_id = job.id)
        db.session.add(application)
        db.session.commit()
        cache.clear()
        return {"message":"Application submitted successfully"},201
        
class StudentApplicationList(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != "student":
            return {"message":"Student access required"},403
        student=Student.query.filter_by(user_id=get_jwt_identity()).first()
        applications = Application.query.filter_by(student_id=student.id).all()
        if not applications:
            return {"message":"No Application Found"},404
        result=[]
        for application in applications:
            result.append({'application_id':application.id,
                           "job_id": application.job.id,
                           "job_title":application.job.title,
                           'company':application.job.company.name,
                           "status":application.status,
                           'offered_salary':application.job.salary,
                           'applied_at':str(application.applied_at),
                           'interview_date': str(application.interview_date) if application.interview_date else None,
                           'feedback': application.feedback
                          })
        return result,200

class StudentPlacementHistory(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get('role') != "student":
            return {"message":"Student access required"},403
        
        student = Student.query.filter_by(user_id=get_jwt_identity()).first()
        applications = Application.query.filter_by(
            student_id=student.id,
            status="selected"
        ).all()

        result = []

        for application in applications:
            placement = application.placement
            if placement:
                result.append({
                    "company": application.job.company.name,
                    "job_title": application.job.title,
                    "offered_salary": placement.offered_salary,
                    "joining_date": str(placement.joining_date)
                })
        return result, 200

