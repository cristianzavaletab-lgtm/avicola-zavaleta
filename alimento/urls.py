from django.urls import path
from . import views

urlpatterns = [
    path('', views.gestion_alimento, name='gestion_alimento'),
    path('registrar/', views.registrar_compra, name='registrar_compra'),
]