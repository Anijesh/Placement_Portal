from extensions import db
from datetime import datetime

class application(db.Models):
    __tablename__='applications'
    id = db.Column(db.Integer,primary_key ='True')
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    status=db.Column(db.String(25),default = 'Applied')
    applied_at = db.Column(db.DateTime,default = datetime.utcnow)
    
    student = db.relationship("Student", backref="applications")
