from extensions import db

class Company(db.models):
    __tablename__='companies'
    id = db.Column(db.Integer,primary_key='True')
    user_id = db.Column(db.Integer,db.ForiegnKey('users.id'),nullable ="False")
    name = db.Column(db.String(200),nullable = "False")
    industry= db.Column(db.String(100))
    website = db.Column(db.String(255))
    approval_status = db.Column(db.String(20), default="Pending")
    location = db.Column(db.String(50),nullable='False')

    user = db.relationship("User", backref=db.backref("company", uselist=False))