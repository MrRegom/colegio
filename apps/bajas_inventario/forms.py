"""
Formularios del módulo de bajas de inventario.

Define los formularios para la gestión de bajas de activos,
siguiendo las mejores prácticas de Django con type hints completos.
"""
from __future__ import annotations

from typing import Any

from django import forms

from .models import BajaInventario, MotivoBaja
from apps.activos.models import Activo, Ubicacion


class MotivoBajaForm(forms.ModelForm):
    """Formulario para crear y editar motivos de baja."""

    class Meta:
        model = MotivoBaja
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: OBS'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Obsolescencia'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del motivo...'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class BajaInventarioForm(forms.ModelForm):
    """
    Formulario para crear/editar bajas de inventario.

    El solicitante se asigna automáticamente en la vista.
    """

    class Meta:
        model = BajaInventario
        fields = [
            'activo', 'numero', 'fecha_baja', 'motivo',
            'ubicacion', 'observaciones'
        ]
        widgets = {
            'activo': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'numero': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Número de baja'}
            ),
            'fecha_baja': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'motivo': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'ubicacion': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Observaciones adicionales (opcional)'
                }
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inicializa el formulario y configura querysets filtrados."""
        super().__init__(*args, **kwargs)

        # Filtrar solo registros activos
        self.fields['motivo'].queryset = MotivoBaja.objects.filter(
            activo=True, eliminado=False
        )
        self.fields['activo'].queryset = Activo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria', 'estado')
        self.fields['ubicacion'].queryset = Ubicacion.objects.filter(
            activo=True, eliminado=False
        )


class FiltroBajasForm(forms.Form):
    """Formulario para filtrar bajas de inventario."""

    motivo = forms.ModelChoiceField(
        queryset=MotivoBaja.objects.filter(activo=True, eliminado=False),
        required=False,
        empty_label='Todos los motivos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        label='Desde'
    )

    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        ),
        label='Hasta'
    )

    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Buscar por número, activo...'
            }
        ),
        label='Buscar'
    )
