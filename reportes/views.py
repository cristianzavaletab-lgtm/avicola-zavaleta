from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Produccion, Lote, Alimento  # Ajusta según tus modelos

@login_required  
def dashboard(request):
    # Obtener el lote activo
    try:
        lote_activo = Lote.objects.filter(activo=True).first()
    except:
        lote_activo = None
    
    # Obtener producción de hoy
    hoy = None
    try:
        hoy = Produccion.objects.filter(fecha=timezone.now().date()).first()
    except:
        pass
    
    # Calcular totales semanales
    try:
        semana_pasada = timezone.now() - timezone.timedelta(days=7)
        produccion_semanal = Produccion.objects.filter(fecha__gte=semana_pasada)
        
        total_buenos = sum([p.huevos_buenos for p in produccion_semanal])
        total_rotos = sum([p.huevos_rotos for p in produccion_semanal])
        total_defectuosos = sum([p.huevos_defectuosos for p in produccion_semanal])
        
        # Calcular ganancia (ejemplo: S/0.30 por huevo bueno)
        ganancia_semanal = total_buenos * 0.30
        
        # Calcular rendimiento (ejemplo)
        total_huevos = total_buenos + total_rotos + total_defectuosos
        rendimiento = (total_buenos / total_huevos * 100) if total_huevos > 0 else 0
        
    except:
        total_buenos = 0
        total_rotos = 0
        total_defectuosos = 0
        ganancia_semanal = 0
        rendimiento = 0
    
    # Obtener alimento restante
    try:
        alimento_restante = Alimento.objects.first().cantidad_kg if Alimento.objects.exists() else 0
    except:
        alimento_restante = 0
    
    # Generar alertas
    alertas = []
    if alimento_restante < 50:
        alertas.append({
            'tipo': 'warning',
            'icono': 'exclamation-triangle',
            'titulo': 'Alimento Bajo',
            'mensaje': f'Solo quedan {alimento_restante}kg de alimento'
        })
    
    context = {
        'lote_activo': lote_activo,
        'hoy': hoy,
        'huevos_buenos': total_buenos,
        'huevos_rotos': total_rotos,
        'huevos_defectuosos': total_defectuosos,
        'alimento_restante': alimento_restante,
        'ganancia_semanal': ganancia_semanal,
        'rendimiento': round(rendimiento, 2),
        'alertas': alertas,
    }
    
    return render(request, 'dashboard.html', context)

@login_required  
def reportes(request):
    return render(request, 'reportes/reportes.html')

@login_required
def reporte_pdf(request):
    return render(request, 'reportes/reporte_pdf.html')