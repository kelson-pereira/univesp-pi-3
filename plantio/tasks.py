from celery import shared_task
from django.http import HttpRequest
from .views import scheduler_controls

@shared_task
def scheduler():
    # Simula uma requisição GET
    request = HttpRequest()
    request.method = 'GET'
    return scheduler_controls(request).content