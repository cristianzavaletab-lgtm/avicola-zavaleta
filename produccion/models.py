from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class GallinaLote(models.Model):
    nombre_lote = models.CharField(max_length=100)
    cantidad_gallinas = models.IntegerField(default=50)
    fecha_inicio = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre_lote} - {self.cantidad_gallinas} gallinas"

class ProduccionDiaria(models.Model):
    lote = models.ForeignKey(GallinaLote, on_delete=models.CASCADE)
    fecha = models.DateField()
    huevos_buenos = models.IntegerField(default=0)
    huevos_rotos = models.IntegerField(default=0)
    huevos_defectuosos = models.IntegerField(default=0)
    celdas_vendidas = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['lote', 'fecha']
        ordering = ['-fecha']
    
    @property
    def total_huevos(self):
        return self.huevos_buenos + self.huevos_rotos + self.huevos_defectuosos
    
    @property
    def ingreso_calculado(self):
        """Calcula el ingreso basado en HUeVOS BUENOS"""
        precio_huevo = 0.30  # S/0.30 por huevo bueno
        return self.huevos_buenos * precio_huevo
    
    def __str__(self):
        return f"Producción {self.lote} - {self.fecha}"

class Configuracion(models.Model):
    clave = models.CharField(max_length=50, unique=True)
    valor = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.clave}: {self.valor}"