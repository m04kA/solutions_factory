import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'solutions_factory.settings')

app = Celery("solutions_factory")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
