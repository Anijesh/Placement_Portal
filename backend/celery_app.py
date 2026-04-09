from celery import Celery
from app import create_app
import time

from celery.schedules import crontab

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['tasks']
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
    beat_schedule={
        'daily-interview-reminders': {
            'task': 'tasks.send_daily_reminders',
            'schedule': crontab(hour=2, minute=21), 
        },
        'monthly-placement-reports': {
            'task': 'tasks.generate_monthly_report',
            'schedule': crontab(day_of_month='10', hour=2, minute=22), 
        }
    }
)

flask_app = create_app()