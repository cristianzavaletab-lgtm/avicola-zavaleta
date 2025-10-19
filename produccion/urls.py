from django.urls import path
from . import views

# SIN app_name - para usar sin namespace
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registro_produccion, name='registro_produccion'),
    path('historial/', views.historial_produccion, name='historial_produccion'),
]