from extensions import db
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key='True')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable='False')
    branch_id= db.Column(db.Integer,db.ForeignKey('branch.id'),nullable='False')
    cgpa= db.Column(db.Float,nullable='False')
    graduation_year= db.Column(db.Intege,nullable='False')
    skills = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("student", uselist=False))
    branch = db.relationship("Branch", backref="students")

