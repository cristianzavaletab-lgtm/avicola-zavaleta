from django import forms
from .models import ProduccionDiaria

class ProduccionDiariaForm(forms.ModelForm):
    class Meta:
        model = ProduccionDiaria
        fields = ['lote', 'fecha', 'huevos_buenos', 'huevos_rotos', 'huevos_defectuosos', 'celdas_vendidas']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'required': True
            }),
            'huevos_buenos': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'placeholder': '0',
                'value': 0,
                'required': True
            }),
            'huevos_rotos': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'placeholder': '0',
                'value': 0,
                'required': True
            }),
            'huevos_defectuosos': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'placeholder': '0',
                'value': 0,
                'required': True
            }),
            'celdas_vendidas': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'placeholder': '0',
                'value': 0,
                'required': True
            }),
            'lote': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        labels = {
            'huevos_buenos': '🥚 Huevos Buenos',
            'huevos_rotos': '💔 Huevos Rotos', 
            'huevos_defectuosos': '⚡ Huevos Defectuosos',
            'celdas_vendidas': '💰 Celdas Vendidas',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar lotes activos
        self.fields['lote'].queryset = self.fields['lote'].queryset.filter(activo=True)