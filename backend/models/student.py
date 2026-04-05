from extensions import db
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key='True')
    name = db.Column(db.String(100),nullable='False')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable='False')
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"), nullable=False)
    cgpa= db.Column(db.Float,nullable='False')
    graduation_year= db.Column(db.Integer,nullable='False')
    skills = db.Column(db.Text)
    experience = db.Column(db.Text, nullable = True)
    resume_link = db.Column(db.String(255), nullable = True)

    user = db.relationship("User", backref=db.backref("student", uselist=False))
    branch = db.relationship("Branch", backref="students")

