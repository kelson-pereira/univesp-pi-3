import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'univesp_pi_3.settings')

app = Celery('univesp_pi_3')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Agenda periódica
app.conf.beat_schedule = {
    'scheduler-beat': {
        'task': 'plantio.tasks.scheduler',
        'schedule': crontab(minute='*'),  # A cada minuto
    },
}