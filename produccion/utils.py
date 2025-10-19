from .models import Configuracion

def obtener_precio_celda():
    """Obtiene el precio de la celda desde la configuración"""
    try:
        config = Configuracion.objects.get(clave='precio_celda')
        return float(config.valor)
    except (Configuracion.DoesNotExist, ValueError):
        return 12.00  # Precio por defecto

def obtener_consumo_diario():
    """Obtiene el consumo diario de alimento desde la configuración"""
    try:
        config = Configuracion.objects.get(clave='consumo_diario_kg')
        return float(config.valor)
    except (Configuracion.DoesNotExist, ValueError):
        return 2.67  # Consumo por defecto para 50 gallinas