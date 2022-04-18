import os
from celery import Celery
import logging

logger = logging.getLogger("mailing")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'solutions_factory.settings')

logger.info("Create app celery: name - solutions_factory")
app = Celery("solutions_factory")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
