# cargar_datos_iniciales.py
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avicola.settings')
django.setup()

from produccion.models import GallinaLote, Configuracion
from django.contrib.auth import get_user_model

Usuario = get_user_model()

def cargar_datos():
    print("🚀 Cargando datos iniciales para Avícola Zavaleta...")
    
    # Crear lote inicial
    lote, created = GallinaLote.objects.get_or_create(
        nombre_lote="Lote Principal",
        defaults={
            'cantidad_gallinas': 50,
            'fecha_inicio': date.today(),
            'activo': True
        }
    )
    
    if created:
        print("✅ Lote principal creado - 50 gallinas")
    else:
        print("ℹ️ Lote principal ya existe")
    
    # Configuraciones iniciales
    configs = [
        ('precio_celda', '12.00', 'Precio por celda de 30 huevos'),
        ('consumo_diario_kg', '2.67', 'Consumo diario de alimento en kg para 50 gallinas'),
        ('alerta_dias_alimento', '3', 'Días de alerta para alimento bajo'),
        ('huevos_por_celda', '30', 'Cantidad de huevos por celda'),
    ]
    
    for clave, valor, desc in configs:
        config, created = Configuracion.objects.get_or_create(
            clave=clave,
            defaults={'valor': valor, 'descripcion': desc}
        )
        if created:
            print(f"✅ Configuración '{clave}' creada: {valor}")
        else:
            print(f"ℹ️ Configuración '{clave}' ya existe")
    
    # Crear usuario encargada de ejemplo
    try:
        encargada, created = Usuario.objects.get_or_create(
            username='maria',
            defaults={
                'first_name': 'María',
                'last_name': 'Gonzales',
                'email': 'maria@avicolazavaleta.com',
                'rol': 'encargada',
                'is_staff': False
            }
        )
        if created:
            encargada.set_password('123')
            encargada.save()
            print("✅ Usuario encargada 'maria' creado (contraseña: 123)")
        else:
            print("ℹ️ Usuario encargada ya existe")
    except Exception as e:
        print(f"⚠️ Error creando usuario encargada: {e}")
    
    print("🎉 ¡Datos iniciales cargados exitosamente!")
    print("\n📋 Usuarios disponibles:")
    print("   👑 admin (Dueño) - contraseña: la que creaste")
    print("   👩 maria (Encargada) - contraseña: 123")

if __name__ == '__main__':
    cargar_datos()