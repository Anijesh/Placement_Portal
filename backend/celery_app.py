from celery import Celery
from app import create_app
import time

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

flask_app = create_app()

@celery.task()
def example_task():
    with flask_app.app_context():
        print("Executing example task...")
        time.sleep(5)
        print("Example task completed.")