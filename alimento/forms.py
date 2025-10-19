from django import forms
from .models import CompraAlimento

class CompraAlimentoForm(forms.ModelForm):
    class Meta:
        model = CompraAlimento
        fields = ['tipo', 'cantidad_kg', 'costo_total', 'fecha_compra', 'proveedor']
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cantidad_kg': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.1'}),
            'costo_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
        }