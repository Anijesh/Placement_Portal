from celery_app import celery, flask_app
from models import Application, Placement, Job, User, Student, Company
from extensions import db
from datetime import date, datetime, timedelta
from mail import send_email
import csv
import os

@celery.task
def send_daily_reminders():
    with flask_app.app_context():
        today = date.today()
        tomorrow = today + timedelta(days=1)
    
        closing_jobs = Job.query.filter(Job.status == 'approved', Job.deadline == tomorrow).all()

        students = Student.query.all()
        sent_count = 0
        
        for student in students:
            for job in closing_jobs:
                has_applied = Application.query.filter_by(student_id=student.id, job_id=job.id).first()
                if has_applied:
                    continue
                
                if job.eligible_branches and student.branch not in job.eligible_branches:
                    continue
                    
                student_email = student.user.email
                subject = f"Reminder: Deadline for {job.company.name} closes tomorrow!"
                body = f"Hello {student.name},\n\nThe application deadline for the {job.title} role at {job.company.name} is tomorrow ({tomorrow}).\n\nLog in to your dashboard to submit your application!"
                
                send_email(to_email=student_email, subject=subject, body=body)
                sent_count += 1
        

        applications = Application.query.filter(
            Application.status == 'interview_scheduled'
        ).all()
        
        interview_sent_count = 0
        for app in applications:
            if not app.interview_date:
                continue
                
            if app.interview_date.date() >= today:
                student_email = app.student.user.email
                subject = f"Reminder: Upcoming Interview with {app.job.company.name}!"
                body = f"Hello {app.student.name},\n\nThis is a friendly reminder that you have an interview scheduled for the {app.job.title} role at {app.job.company.name} on {app.interview_date.date()}.\n\nGood luck!"
                
                send_email(to_email=student_email, subject=subject, body=body)
                interview_sent_count += 1
            
        return f"Sent {sent_count} deadline reminders and {interview_sent_count} interview reminders."

@celery.task
def generate_monthly_report():
    with flask_app.app_context():
        
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            return "No admin found"

        total_drives = Job.query.count()
        total_applied = Application.query.count()
        total_selected = Placement.query.count()

        subject = "Monthly Placement Activity Report"
        body = "Please view the attached HTML version."
        
        html_body = f"""
        <html>
            <body>
                <h2>Institute Placement Report</h2>
                <hr>
                <p><strong>Total Placement Drives Conducted:</strong> {total_drives}</p>
                <p><strong>Total Applications Processed:</strong> {total_applied}</p>
                <p><strong>Total Students Placed:</strong> {total_selected}</p>
                <br>
                <p><em>Generated automatically by PPA-V2 System</em></p>
            </body>
        </html>
        """

        send_email(to_email=admin.email, subject=subject, body=body, html_body=html_body)
        return "Monthly report sent to Admin."

@celery.task
def export_applications_csv(user_id, role, email_to_notify):
    """User-triggered batch job exporting applications as CSV"""
    with flask_app.app_context():
        static_dir = 'static/exports'
        os.makedirs(static_dir, exist_ok=True)
        
        file_name = f"export_{role}_{user_id}_{int(datetime.now().timestamp())}.csv"
        file_path = f"{static_dir}/{file_name}"

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            if role == 'student':
                student = Student.query.filter_by(user_id=user_id).first()
                apps = Application.query.filter_by(student_id=student.id).all()
                writer.writerow(['Student ID', 'Company Name', 'Drive Title', 'Application Status', 'Application Date'])
                
                for app in apps:
                    writer.writerow([
                        student.id, 
                        app.job.company.name, 
                        app.job.title, 
                        app.status, 
                        str(app.applied_at)
                    ])
            
            elif role == 'company':
                company = Company.query.filter_by(user_id=user_id).first()
                jobs = Job.query.filter_by(company_id=company.id).all()
                job_ids = [j.id for j in jobs]
                apps = Application.query.filter(Application.job_id.in_(job_ids)).all()
                writer.writerow(['Student ID', 'Student Name', 'Drive Title', 'Application Status', 'Application Date'])
                
                for app in apps:
                    writer.writerow([
                        app.student.id, 
                        app.student.name, 
                        app.job.title, 
                        app.status, 
                        str(app.applied_at)
                    ])

        subject = "Your CSV Export is Ready"
        body = f"Your requested CSV export has finished processing.\nFilename: {file_name}\nYou can download it from your dashboard."
        send_email(to_email=email_to_notify, subject=subject, body=body)

        return file_name
