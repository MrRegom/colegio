"""
Formularios del módulo de activos.

Define los formularios para la gestión de activos, incluyendo:
- Catálogos: Categorías, Estados, Ubicaciones, Marcas, Talleres, Proveniencias
- Gestión de Activos y Movimientos
"""
from __future__ import annotations

from typing import Any

from django import forms
from django.contrib.auth.models import User

from .models import (
    Activo, CategoriaActivo, EstadoActivo, Ubicacion,
    Proveniencia, Marca, Taller, TipoMovimientoActivo, MovimientoActivo
)


class CategoriaActivoForm(forms.ModelForm):
    """Formulario para crear y editar categorías de activos"""

    class Meta:
        model = CategoriaActivo
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: COMP'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Computadoras'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la categoría...'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class EstadoActivoForm(forms.ModelForm):
    """Formulario para crear y editar estados de activos"""

    class Meta:
        model = EstadoActivo
        fields = ['codigo', 'nombre', 'descripcion', 'color', 'es_inicial', 'permite_movimiento', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: ACTIVO'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Activo'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'color': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'color'}
            ),
            'es_inicial': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'permite_movimiento': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class ActivoForm(forms.ModelForm):
    """
    Formulario para crear y editar activos.

    Los activos son bienes individuales que NO manejan stock.
    Cada activo es único y se rastrea individualmente.
    """

    class Meta:
        model = Activo
        fields = [
            'codigo', 'nombre', 'descripcion',
            'categoria', 'estado', 'marca',
            'lote', 'numero_serie', 'codigo_barras',
            'precio_unitario', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Código único del activo'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombre del activo'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción detallada...'}
            ),
            'categoria': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'estado': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'marca': forms.Select(
                attrs={'class': 'form-select', 'id': 'id_marca'}
            ),
            'lote': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Lote (opcional)'}
            ),
            'numero_serie': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Número de serie'}
            ),
            'codigo_barras': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Dejar vacío para auto-generar desde código'}
            ),
            'precio_unitario': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inicializa el formulario y configura querysets filtrados."""
        super().__init__(*args, **kwargs)
        # Filtrar solo registros activos para los selectores
        self.fields['categoria'].queryset = CategoriaActivo.objects.filter(
            activo=True, eliminado=False
        )
        self.fields['estado'].queryset = EstadoActivo.objects.filter(activo=True)
        self.fields['marca'].queryset = Marca.objects.filter(activo=True, eliminado=False)

        # Marca es opcional
        self.fields['marca'].required = False


class UbicacionForm(forms.ModelForm):
    """Formulario para crear y editar ubicaciones físicas."""

    class Meta:
        model = Ubicacion
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: UB001'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Oficina Principal'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la ubicación...'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class TipoMovimientoActivoForm(forms.ModelForm):
    """Formulario para crear y editar tipos de movimiento."""

    class Meta:
        model = TipoMovimientoActivo
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: ASIG'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Asignación'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class MovimientoActivoForm(forms.ModelForm):
    """
    Formulario para registrar movimientos de activos individuales.

    Cada movimiento registra la trazabilidad del activo:
    ubicación, responsable, taller asociado, proveniencia, etc.
    """

    class Meta:
        model = MovimientoActivo
        fields = [
            'activo', 'tipo_movimiento', 'ubicacion_destino', 'taller',
            'responsable', 'proveniencia', 'observaciones'
        ]
        widgets = {
            'activo': forms.Select(
                attrs={'class': 'form-select', 'id': 'id_activo'}
            ),
            'tipo_movimiento': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'ubicacion_destino': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'taller': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'responsable': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'proveniencia': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales...'}
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inicializa el formulario configurando querysets filtrados."""
        super().__init__(*args, **kwargs)

        # Filtrar solo registros activos
        self.fields['activo'].queryset = Activo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria', 'estado')
        self.fields['tipo_movimiento'].queryset = TipoMovimientoActivo.objects.filter(
            activo=True, eliminado=False
        )
        self.fields['ubicacion_destino'].queryset = Ubicacion.objects.filter(
            activo=True, eliminado=False
        )
        self.fields['taller'].queryset = Taller.objects.filter(
            activo=True, eliminado=False
        )
        self.fields['responsable'].queryset = User.objects.filter(
            is_active=True
        ).order_by('username')
        self.fields['proveniencia'].queryset = Proveniencia.objects.filter(
            activo=True, eliminado=False
        )

        # Campos opcionales
        self.fields['ubicacion_destino'].required = False
        self.fields['taller'].required = False
        self.fields['responsable'].required = False
        self.fields['proveniencia'].required = False


class FiltroActivosForm(forms.Form):
    """Formulario para filtrar activos en la lista"""

    categoria = forms.ModelChoiceField(
        queryset=CategoriaActivo.objects.filter(activo=True, eliminado=False),
        required=False,
        empty_label='Todas las categorías',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    estado = forms.ModelChoiceField(
        queryset=EstadoActivo.objects.filter(activo=True),
        required=False,
        empty_label='Todos los estados',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    buscar = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Buscar por código, nombre, marca...'
            }
        )
    )


class MarcaForm(forms.ModelForm):
    """Formulario para crear y editar marcas de activos."""

    class Meta:
        model = Marca
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: HP'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Hewlett-Packard'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la marca...'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class TallerForm(forms.ModelForm):
    """Formulario para crear y editar talleres de servicio."""

    class Meta:
        model = Taller
        fields = ['codigo', 'nombre', 'descripcion', 'ubicacion', 'responsable', 'observaciones', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: TALL01'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Taller de Mantenimiento'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del taller...'}
            ),
            'ubicacion': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ubicación física del taller'}
            ),
            'responsable': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones...'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inicializa el formulario configurando querysets filtrados."""
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.filter(
            is_active=True
        ).order_by('username')
        self.fields['responsable'].required = False


class ProvenienciaForm(forms.ModelForm):
    """Formulario para crear y editar proveniencias de activos."""

    class Meta:
        model = Proveniencia
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: COMP'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Compra'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la proveniencia...'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
