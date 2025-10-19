from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Lote(models.Model):
    nombre_lote = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre_lote

class Produccion(models.Model):
    fecha = models.DateField(default=timezone.now)
    huevos_buenos = models.IntegerField(default=0)
    huevos_rotos = models.IntegerField(default=0)
    huevos_defectuosos = models.IntegerField(default=0)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    
    def total_huevos(self):
        return self.huevos_buenos + self.huevos_rotos + self.huevos_defectuosos
    
    def __str__(self):
        return f"Producción {self.fecha}"

class Alimento(models.Model):
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Alimento: {self.cantidad_kg}kg"