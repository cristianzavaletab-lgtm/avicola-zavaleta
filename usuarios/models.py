from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('encargada', 'Encargada'),
        ('dueño', 'Dueño'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='encargada')
    telefono = models.CharField(max_length=15, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"