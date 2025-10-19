from django.db import models

class CompraAlimento(models.Model):
    TIPO_ALIMENTO = (
        ('postura', 'Alimento de Postura'),
        ('cebada', 'Cebada'),
        ('maiz', 'Maíz'),
        ('otros', 'Otros'),
    )
    
    tipo = models.CharField(max_length=20, choices=TIPO_ALIMENTO, default='postura')
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateField()
    proveedor = models.CharField(max_length=100, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.cantidad_kg}kg - S/{self.costo_total}"
    
    def get_tipo_display(self):
        """Método para obtener el nombre legible del tipo"""
        return dict(self.TIPO_ALIMENTO).get(self.tipo, self.tipo)