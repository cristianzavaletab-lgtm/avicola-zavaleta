from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import ProduccionDiaria, GallinaLote, Configuracion
from .forms import ProduccionDiariaForm
from alimento.models import CompraAlimento

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    print(f"=== DASHBOARD - FECHA HOY: {hoy} ===")
    
    # Inicializar variables con valores por defecto
    lote_activo = None
    produccion_hoy = None
    alimento_restante = Decimal('0')
    ganancia_semanal = Decimal('0')
    rendimiento = 85
    
    try:
        lote_activo = GallinaLote.objects.filter(activo=True).first()
        print(f"📌 Lote activo: {lote_activo}")
        
        if lote_activo:
            # Producción de hoy
            produccion_hoy = ProduccionDiaria.objects.filter(fecha=hoy, lote=lote_activo).first()
            print(f"📊 Producción hoy: {produccion_hoy}")
            
            if produccion_hoy:
                print(f"🥚 Datos: Buenos={produccion_hoy.huevos_buenos}, Rotos={produccion_hoy.huevos_rotos}, Defectuosos={produccion_hoy.huevos_defectuosos}")
            
            # CÁLCULO DE ALIMENTO CORREGIDO - SIN ERRORES DE TIPO
            compras_alimento = CompraAlimento.objects.all()
            if compras_alimento.exists():
                total_comprado = sum(compra.cantidad_kg for compra in compras_alimento)
                print(f"🌾 Total alimento comprado: {total_comprado}kg")
                
                # Consumo estimado: 0.12kg por gallina por día (convertido a Decimal)
                consumo_diario = Decimal(str(lote_activo.cantidad_gallinas * 0.12))
                dias_transcurridos = (hoy - lote_activo.fecha_inicio).days
                alimento_consumido = consumo_diario * Decimal(str(dias_transcurridos))
                alimento_restante = max(total_comprado - alimento_consumido, Decimal('0'))
                print(f"📦 Alimento restante: {alimento_restante}kg")
            else:
                alimento_restante = Decimal('0')
                print("🌾 No hay compras de alimento registradas")
            
            # Producción de la última semana
            fecha_inicio_semana = hoy - timedelta(days=7)
            produccion_semana = ProduccionDiaria.objects.filter(
                fecha__range=[fecha_inicio_semana, hoy],
                lote=lote_activo
            )
            
            # CALCULAR GANANCIA SEMANAL CORREGIDO
            if produccion_semana.exists():
                # Sumar todos los ingresos calculados de la semana
                for produccion in produccion_semana:
                    ganancia_semanal += Decimal(str(produccion.ingreso_calculado))
                print(f"💰 Producción semanal encontrada: {produccion_semana.count()} registros")
                print(f"💰 Ganancia semanal: S/{ganancia_semanal}")
            else:
                print("💰 No hay producción en la última semana")
            
            # Calcular rendimiento real si hay producción hoy
            if produccion_hoy and produccion_hoy.total_huevos > 0:
                rendimiento = (produccion_hoy.huevos_buenos / produccion_hoy.total_huevos) * 100
                rendimiento = round(rendimiento, 1)
                print(f"📈 Rendimiento calculado: {rendimiento}%")
        
    except Exception as e:
        print(f"❌ ERROR EN DASHBOARD: {e}")
        import traceback
        print(f"🔍 Detalle del error: {traceback.format_exc()}")
    
    # Convertir a float para el template (evita problemas de serialización)
    context = {
        'lote_activo': lote_activo,
        'hoy': produccion_hoy,
        'alimento_restante': float(alimento_restante),
        'ganancia_semanal': float(ganancia_semanal),
        'rendimiento': rendimiento,
    }
    
    print(f"=== CONTEXTO FINAL ===")
    print(f"lote_activo: {context['lote_activo']}")
    print(f"hoy: {context['hoy']}")
    print(f"alimento_restante: {context['alimento_restante']}kg")
    print(f"ganancia_semanal: S/{context['ganancia_semanal']}")
    print(f"rendimiento: {context['rendimiento']}%")
    
    return render(request, 'dashboard.html', context)

@login_required
def registro_produccion(request):
    print("=== INICIANDO VISTA REGISTRO ===")
    
    if request.method == 'POST':
        print("📨 MÉTODO POST RECIBIDO")
        form = ProduccionDiariaForm(request.POST)
        print(f"✅ Formulario creado")
        print(f"📊 Datos POST: {dict(request.POST)}")
        
        if form.is_valid():
            print("✅ FORMULARIO VÁLIDO")
            produccion = form.save(commit=False)
            
            # Establecer valores por defecto si están vacíos
            produccion.huevos_buenos = produccion.huevos_buenos or 0
            produccion.huevos_rotos = produccion.huevos_rotos or 0
            produccion.huevos_defectuosos = produccion.huevos_defectuosos or 0
            produccion.celdas_vendidas = produccion.celdas_vendidas or 0
            
            print(f"📅 Fecha: {produccion.fecha}")
            print(f"🥚 Buenos: {produccion.huevos_buenos}")
            print(f"💔 Rotos: {produccion.huevos_rotos}")
            print(f"⚡ Defectuosos: {produccion.huevos_defectuosos}")
            print(f"💰 Celdas: {produccion.celdas_vendidas}")
            print(f"🏷️ Lote: {produccion.lote}")
            
            # Buscar si ya existe registro
            existe = ProduccionDiaria.objects.filter(
                fecha=produccion.fecha,
                lote=produccion.lote
            ).first()
            
            if existe:
                print("🔄 REGISTRO EXISTENTE ENCONTRADO - ACTUALIZANDO")
                # Actualizar el registro existente
                existe.huevos_buenos = produccion.huevos_buenos
                existe.huevos_rotos = produccion.huevos_rotos
                existe.huevos_defectuosos = produccion.huevos_defectuosos
                existe.celdas_vendidas = produccion.celdas_vendidas
                existe.save()
                print("✅ REGISTRO ACTUALIZADO EXITOSAMENTE")
                messages.success(request, 'Producción actualizada exitosamente!')
            else:
                print("🆕 CREANDO NUEVO REGISTRO")
                produccion.save()
                print("✅ NUEVO REGISTRO GUARDADO EXITOSAMENTE")
                messages.success(request, 'Producción registrada exitosamente!')
            
            return redirect('dashboard')
        else:
            print("❌ FORMULARIO INVÁLIDO")
            print(f"🚨 Errores: {form.errors}")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        print("📝 MÉTODO GET - MOSTRANDO FORMULARIO")
        lote_activo = GallinaLote.objects.filter(activo=True).first()
        initial_data = {
            'fecha': timezone.now().date(),
            'lote': lote_activo,
            'huevos_buenos': 0,
            'huevos_rotos': 0,
            'huevos_defectuosos': 0,
            'celdas_vendidas': 0,
        }
        form = ProduccionDiariaForm(initial=initial_data)
        print(f"📋 Formulario inicializado con: {initial_data}")
    
    return render(request, 'produccion/registro.html', {'form': form})

@login_required
def historial_produccion(request):
    try:
        lote_activo = GallinaLote.objects.filter(activo=True).first()
        produccion = ProduccionDiaria.objects.filter(lote=lote_activo).order_by('-fecha')[:30]
    except Exception as e:
        lote_activo = None
        produccion = []
    
    context = {
        'produccion': produccion,
        'lote_activo': lote_activo,
    }
    return render(request, 'produccion/historial.html', context)