from extensions import db

class Placement(db.Model):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False, unique=True
    )
    offered_salary = db.Column(db.Float)
    joining_date = db.Column(db.Date)

    application = db.relationship("Application", backref=db.backref("placement", uselist=False))