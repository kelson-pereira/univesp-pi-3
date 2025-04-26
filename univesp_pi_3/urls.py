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
from plantio.views import home, login_view, logout_view, reset_view, signup_view, led_status, toggle_led, led_control_view, sensor_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("reset/", views.reset_view, name="reset"),
    path("signup/", views.signup_view, name="signup"),
    path("favicon.ico", RedirectView.as_view(url="/static/imagens/favicon.ico", permanent=True)),
    path("dashboard/<str:id>/", views.dashboard, name="dashboard"),
    path("update/", views.update, name="update"),
    path('update-schedule/', views.update_schedule, name='update_schedule'),
    path('update-schedule-status/', views.update_schedule_status, name='update_schedule_status'),
    path('update-control-status/', views.update_control_status, name='update_control_status'),
]
