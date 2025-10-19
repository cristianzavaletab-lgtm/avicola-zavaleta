from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes, name='reportes'),
    path('pdf/', views.reporte_pdf, name='reporte_pdf'),
]