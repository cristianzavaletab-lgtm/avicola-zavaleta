from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CompraAlimento
from .forms import CompraAlimentoForm

@login_required
def gestion_alimento(request):
    compras = CompraAlimento.objects.all().order_by('-fecha_compra')
    
    # Cálculos de alimento
    total_comprado = sum(compra.cantidad_kg for compra in compras)
    costo_total = sum(compra.costo_total for compra in compras)
    
    # Calcular costo promedio
    if total_comprado > 0:
        costo_promedio = costo_total / total_comprado
    else:
        costo_promedio = 0
    
    context = {
        'compras': compras,
        'total_comprado': total_comprado,
        'costo_total': costo_total,
        'costo_promedio': costo_promedio,
        'form': CompraAlimentoForm()
    }
    return render(request, 'alimento/gestion.html', context)

@login_required
def registrar_compra(request):
    if request.method == 'POST':
        form = CompraAlimentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compra de alimento registrada exitosamente!')
            return redirect('gestion_alimento')
    else:
        form = CompraAlimentoForm()
    
    return render(request, 'alimento/registrar_compra.html', {'form': form})