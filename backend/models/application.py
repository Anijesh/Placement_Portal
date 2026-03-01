from extensions import db
from datetime import datetime

class application(db.Models):
    __tablename__='applications'
    id = db.Column(db.Integer,primary_key ='True')
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    status=db.Column(db.String(25),default = 'Applied')
    applied_at = db.Column(db.DateTime,default = datetime.utcnow)
    
    student = db.relationship("Student", backref="applications")
    __table_args__ = (
        db.UniqueConstraint("student_id", "job_id", name="unique_student_job"),
    )
    job = db.relationship("Job", backref="applications")
