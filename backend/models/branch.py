from extensions import db

class branch(db.Models):
    __tablename__='bramches'
    id = db.Column(db.Integer,unique = 'True')
    name =db.Column(db.String(100),unique=True,nullable='False')
