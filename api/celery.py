import os

from celery import Celery
import dotenv
dotenv.load_dotenv()

app = Celery("api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
