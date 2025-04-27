"""
Configurações de URL para projeto univesp_pi_3.

A lista `urlpatterns` roteia URLs para visualizações. Para mais informações consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Exemplos:
Função views
    1. Adicione a importação:  from my_app import views
    2. Adicione a URL em urlpatterns:  path('', views.home, name='home')
Views baseada em uma classe:
    1. Adicione a importação:  from other_app.views import Home
    2. Adicione a URL em urlpatterns:  path('', Home.as_view(), name='home')
Incluindo outra configuração de URL:
    1. Importe a função include(): from django.urls import include, path
    2. Adicione a URL em urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from plantio import views
from plantio.views import home, led_status, toggle_led, led_control_view, sensor_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("favicon.ico", RedirectView.as_view(url="/static/imagens/favicon.ico", permanent=True)),
    path("led/status/", views.led_status, name="led_status"),
    path("led/toggle/", views.toggle_led, name="toggle_led"),
    path("led/control/", views.led_control_view, name="led_control"),
    path("controls/", views.controls, name='controls'),
    path("sensors/", views.sensor_data, name="sensor_data"),
    path("dashboard/<str:id>/", views.dashboard, name="dashboard"),
    path("update/", views.update, name="update"),
    path('update-schedule/', views.update_schedule, name='update_schedule'),
]
