from django.shortcuts import render
from django.views.generic.base import RedirectView

# Crie suas visualizações aqui.

def home(request):
    return render(request, 'home.html')