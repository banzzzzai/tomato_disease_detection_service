from kombu import Queue
from celery import current_app as current_celery_app, Celery
from asynchrony.celery_app.celery_config import settings


def create_celery():
    celery_app = Celery("recognition")
    celery_app.config_from_object(settings, namespace="CELERY")
    celery_app.task_queues= (
        Queue('image_recognition', routing_key="image_recognition"),
    )
    return celery_app
