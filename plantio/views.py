from django.shortcuts import render
from django.views.generic.base import RedirectView

# Crie suas visualizações aqui.

favicon = RedirectView.as_view(url='/static/imagens/favicon.ico', permanent=True)

def home(request):
    return render(request, 'home.html')