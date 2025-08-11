from django import forms
from .models import Asistencia, Fecha
from django.utils import timezone

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['nickname', 'apodo', 'puntos', 'fecha', 'avatar']
        widgets = {
            'fecha': forms.DateTimeInput(
                attrs={'class': 'custom-input-full', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir atributos al campo de nickname
        self.fields['nickname'].widget.attrs.update({
            'class': 'custom-input-full',
            'placeholder': 'Ingresa tu nickname'
        })
        
        # Añadir atributos al campo de apodo
        self.fields['apodo'].widget.attrs.update({
            'class': 'custom-input-full',
            'placeholder': 'Ingresa un apodo (opcional)'
        })
        
        # Añadir atributos al campo de puntos
        self.fields['puntos'].widget.attrs.update({
            'class': 'custom-input-full',
            'placeholder': 'Puntos obtenidos hoy'
        })
        
        # Por defecto, establecer la fecha y hora actual
        self.fields['fecha'].initial = timezone.now()


class FechaForm(forms.ModelForm):
    class Meta:
        model = Fecha
        fields = ['nombre', 'fecha', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        # Verificar si ya existe una fecha con el mismo valor
        if Fecha.objects.filter(fecha=fecha).exists():
            raise forms.ValidationError("Ya existe un registro para esta fecha")
        return fecha
    