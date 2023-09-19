import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'savanah.settings')
app = Celery('savanah', broker="pyamqp://guest@localhost//")
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
