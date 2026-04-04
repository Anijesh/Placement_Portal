from extensions import db
from datetime import datetime

job_branch = db.Table(
    "job_branch",
    db.Column("job_id", db.Integer, db.ForeignKey("jobs.id"), primary_key=True),
    db.Column("branch_id", db.Integer, db.ForeignKey("branches.id"), primary_key=True),
)


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    min_cgpa = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    salary = db.Column(db.String(100))
    status = db.Column(db.String(20), default="pending")  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("Company", backref="jobs")
    eligible_branches = db.relationship(
        "Branch",
        secondary=job_branch,
        backref="jobs"
    )