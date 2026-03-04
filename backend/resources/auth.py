from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from models import User, Student, Company
from extensions import db

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {"message" :" Email already exist"},400
        role = data.get('role','student')

        if role=='admin':
            return {"message": "Admin registration not allowed"}, 403
        
        user=User(email=data['email'],role=role)
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush() 

        if role == 'student':
            student = Student(
                name=data.get('name'),
                user_id=user.id,
                branch_id=data.get('branch_id'),
                cgpa=data.get('cgpa'),
                graduation_year=data.get('graduation_year'),
                skills=data.get('skills')
            )
            db.session.add(student)
        elif role == 'company':
            company = Company(
                user_id=user.id,
                name=data.get('name'),
                industry=data.get('industry', ''),
                website=data.get('website', ''),
                location=data.get('location')
            )
            db.session.add(company)

        db.session.commit()
        return {'message':"registration successfully"}
    
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return {'message': 'Account not exist'}, 404

        if not user.check_password(data['password']):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role}
        )

        return {
            "access_token": access_token,
            "role": user.role
        }, 200