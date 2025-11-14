"""
Formularios para el módulo de inventario.
"""

from django import forms
from django.contrib.auth.models import User
from .models import (
    Taller, TipoEquipo, Equipo, MantenimientoEquipo,
    Marca, Modelo, NombreArticulo, SectorInventario
)
from apps.bodega.models import Bodega
from apps.compras.models import EstadoOrdenCompra, EstadoRecepcion
from apps.activos.models import Proveniencia
from apps.solicitudes.models import Departamento


class TallerForm(forms.ModelForm):
    """Formulario para Taller"""
    
    class Meta:
        model = Taller
        fields = [
            'codigo', 'nombre', 'descripcion', 'ubicacion',
            'responsable', 'capacidad_maxima', 'equipamiento', 'observaciones',
            'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control'}),
            'equipamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TipoEquipoForm(forms.ModelForm):
    """Formulario para TipoEquipo"""
    
    class Meta:
        model = TipoEquipo
        fields = [
            'codigo', 'nombre', 'descripcion',
            'requiere_mantenimiento', 'periodo_mantenimiento_dias', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'requiere_mantenimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'periodo_mantenimiento_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EquipoForm(forms.ModelForm):
    """Formulario para Equipo"""
    
    class Meta:
        model = Equipo
        fields = [
            'codigo', 'nombre', 'descripcion', 'tipo', 'marca', 'modelo',
            'numero_serie', 'fecha_adquisicion', 'valor_adquisicion',
            'estado', 'ubicacion_actual', 'responsable', 'taller',
            'fecha_ultimo_mantenimiento', 'fecha_proximo_mantenimiento',
            'observaciones', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_adquisicion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_adquisicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion_actual': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'taller': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ultimo_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_proximo_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MantenimientoEquipoForm(forms.ModelForm):
    """Formulario para MantenimientoEquipo"""
    
    class Meta:
        model = MantenimientoEquipo
        fields = [
            'equipo', 'fecha_mantenimiento', 'tipo_mantenimiento',
            'descripcion', 'realizado_por', 'costo',
            'proximo_mantenimiento', 'observaciones'
        ]
        widgets = {
            'equipo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_mantenimiento': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'realizado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'proximo_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ==================== FORMULARIOS PARA OTROS MODELOS ====================

class BodegaForm(forms.ModelForm):
    """Formulario para Bodega"""
    
    class Meta:
        model = Bodega
        fields = ['codigo', 'nombre', 'descripcion', 'responsable', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EstadoOrdenCompraForm(forms.ModelForm):
    """Formulario para EstadoOrdenCompra"""
    
    class Meta:
        model = EstadoOrdenCompra
        fields = [
            'codigo', 'nombre', 'descripcion', 'color',
            'es_inicial', 'es_final', 'permite_edicion', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'es_inicial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_final': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permite_edicion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EstadoRecepcionForm(forms.ModelForm):
    """Formulario para EstadoRecepcion"""
    
    class Meta:
        model = EstadoRecepcion
        fields = [
            'codigo', 'nombre', 'descripcion', 'color',
            'es_inicial', 'es_final', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'es_inicial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_final': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProvenienciaForm(forms.ModelForm):
    """Formulario para Proveniencia"""
    
    class Meta:
        model = Proveniencia
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartamentoForm(forms.ModelForm):
    """Formulario para Departamento"""
    
    class Meta:
        model = Departamento
        fields = ['codigo', 'nombre', 'descripcion', 'responsable', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==================== FORMULARIOS PARA CATÁLOGOS DE PRODUCTOS ====================

class MarcaForm(forms.ModelForm):
    """Formulario para Marca"""
    
    class Meta:
        model = Marca
        fields = ['codigo', 'nombre', 'descripcion', 'logo_url', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo_url': forms.URLInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ModeloForm(forms.ModelForm):
    """Formulario para Modelo"""
    
    class Meta:
        model = Modelo
        fields = ['codigo', 'nombre', 'marca', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-select', 'id': 'id_marca'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo marcas activas
        self.fields['marca'].queryset = Marca.objects.filter(activo=True, eliminado=False)


class NombreArticuloForm(forms.ModelForm):
    """Formulario para Nombre de Artículo"""
    
    class Meta:
        model = NombreArticulo
        fields = ['codigo', 'nombre', 'descripcion', 'categoria_recomendada', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria_recomendada': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SectorInventarioForm(forms.ModelForm):
    """Formulario para Sector de Inventario"""
    
    class Meta:
        model = SectorInventario
        fields = ['codigo', 'nombre', 'descripcion', 'responsable', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

