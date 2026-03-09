from extensions import db
from datetime import datetime
class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    status = db.Column(db.String(20), default="applied")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("student_id", "job_id", name="unique_student_job"),
    )

    student = db.relationship("Student", backref="applications")
    job = db.relationship("Job", backref="applications")