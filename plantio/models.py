from django.db import models

# Crie seus modelos aqui.

class Led(models.Model):
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)