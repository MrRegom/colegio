from django import forms
from django.forms import inlineformset_factory
from .models import (
    Solicitud, DetalleSolicitud, TipoSolicitud, EstadoSolicitud,
    Departamento, Area, Equipo
)
from apps.activos.models import Activo
from apps.bodega.models import Bodega, Articulo


class SolicitudForm(forms.ModelForm):
    """Formulario para crear y editar solicitudes"""

    class Meta:
        model = Solicitud
        fields = [
            'tipo_solicitud',
            'fecha_requerida',
            'titulo_actividad',
            'objetivo_actividad',
            'departamento',
            'area',
            'equipo',
            'bodega_origen',
            'area_solicitante',
            'motivo',
            'observaciones'
        ]
        widgets = {
            'fecha_requerida': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'tipo_solicitud': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'titulo_actividad': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Taller de Capacitación Docente'
                }
            ),
            'objetivo_actividad': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Describa el objetivo de la actividad...'
                }
            ),
            'departamento': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'area': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'equipo': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'bodega_origen': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'area_solicitante': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Departamento de TI'}
            ),
            'motivo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Describa el motivo de la solicitud...'
                }
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Observaciones adicionales (opcional)...'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo tipos de solicitud activos
        self.fields['tipo_solicitud'].queryset = TipoSolicitud.objects.filter(activo=True)
        # Filtrar solo bodegas activas
        self.fields['bodega_origen'].queryset = Bodega.objects.filter(activo=True)
        # Filtrar solo departamentos activos
        self.fields['departamento'].queryset = Departamento.objects.filter(activo=True, eliminado=False)
        # Filtrar solo áreas activas
        self.fields['area'].queryset = Area.objects.filter(activo=True, eliminado=False).select_related('departamento')
        # Filtrar solo equipos activos
        self.fields['equipo'].queryset = Equipo.objects.filter(activo=True, eliminado=False).select_related('departamento')

        # Hacer campos opcionales
        self.fields['bodega_origen'].required = False
        self.fields['departamento'].required = False
        self.fields['area'].required = False
        self.fields['equipo'].required = False
        self.fields['titulo_actividad'].required = False
        self.fields['objetivo_actividad'].required = False


class DetalleSolicitudArticuloForm(forms.ModelForm):
    """Formulario para cada línea de detalle de solicitud de ARTÍCULOS"""

    class Meta:
        model = DetalleSolicitud
        fields = ['articulo', 'cantidad_solicitada', 'observaciones']
        widgets = {
            'articulo': forms.Select(
                attrs={'class': 'form-select articulo-select'}
            ),
            'cantidad_solicitada': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0.01',
                    'step': '0.01',
                    'placeholder': '0.00'
                }
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'placeholder': 'Observaciones del artículo (opcional)...'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo artículos activos
        self.fields['articulo'].queryset = Articulo.objects.filter(activo=True).select_related(
            'categoria', 'ubicacion_fisica'
        )


class DetalleSolicitudActivoForm(forms.ModelForm):
    """Formulario para cada línea de detalle de solicitud de BIENES/ACTIVOS"""

    class Meta:
        model = DetalleSolicitud
        fields = ['activo', 'cantidad_solicitada', 'observaciones']
        widgets = {
            'activo': forms.Select(
                attrs={'class': 'form-select activo-select'}
            ),
            'cantidad_solicitada': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0.01',
                    'step': '0.01',
                    'placeholder': '0.00'
                }
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'placeholder': 'Observaciones del bien (opcional)...'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo activos/bienes activos
        # Los activos no tienen unidad_medida, son bienes únicos que se rastrean individualmente
        self.fields['activo'].queryset = Activo.objects.filter(activo=True).select_related(
            'categoria', 'marca', 'estado'
        )


# Formsets separados para Artículos y Activos
DetalleSolicitudArticuloFormSet = inlineformset_factory(
    Solicitud,
    DetalleSolicitud,
    form=DetalleSolicitudArticuloForm,
    extra=5,  # 5 líneas vacías por defecto
    can_delete=False,  # No permite eliminar líneas desde el formset
    min_num=1,  # Mínimo una línea requerida
    validate_min=True
)

DetalleSolicitudActivoFormSet = inlineformset_factory(
    Solicitud,
    DetalleSolicitud,
    form=DetalleSolicitudActivoForm,
    extra=5,  # 5 líneas vacías por defecto
    can_delete=False,  # No permite eliminar líneas desde el formset
    min_num=1,  # Mínimo una línea requerida
    validate_min=True
)


class AprobarSolicitudForm(forms.Form):
    """Formulario para aprobar una solicitud"""

    notas_aprobacion = forms.CharField(
        label='Notas de Aprobación',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese notas o comentarios sobre la aprobación...'
            }
        ),
        required=False
    )

    def __init__(self, *args, solicitud=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.solicitud = solicitud

        # Agregar campos dinámicos para cada detalle
        if solicitud:
            for detalle in solicitud.detalles.all():
                field_name = f'cantidad_aprobada_{detalle.id}'
                # Obtener unidad de medida según tipo
                if detalle.articulo:
                    # Articulo tiene ManyToMany unidades_medida, obtener la primera o mostrar todas
                    unidades = detalle.articulo.unidades_medida.all()
                    if unidades.exists():
                        unidad = ', '.join([u.simbolo for u in unidades])
                    else:
                        unidad = 'unidad'
                else:
                    # Los activos son bienes únicos sin unidad de medida
                    unidad = 'unidad'

                self.fields[field_name] = forms.DecimalField(
                    label=f'Cantidad Aprobada - {detalle.producto_nombre}',
                    max_digits=10,
                    decimal_places=2,
                    min_value=0,
                    max_value=detalle.cantidad_solicitada,
                    initial=detalle.cantidad_solicitada,
                    widget=forms.NumberInput(
                        attrs={
                            'class': 'form-control',
                            'step': '0.01'
                        }
                    ),
                    help_text=f'Solicitada: {detalle.cantidad_solicitada} {unidad}'
                )


class DespacharSolicitudForm(forms.Form):
    """Formulario para despachar una solicitud"""

    notas_despacho = forms.CharField(
        label='Notas de Despacho',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese notas o comentarios sobre el despacho...'
            }
        ),
        required=False
    )

    def __init__(self, *args, solicitud=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.solicitud = solicitud

        # Agregar campos dinámicos para cada detalle
        if solicitud:
            for detalle in solicitud.detalles.all():
                field_name = f'cantidad_despachada_{detalle.id}'
                max_cantidad = detalle.cantidad_aprobada if detalle.cantidad_aprobada > 0 else detalle.cantidad_solicitada

                # Obtener unidad de medida según tipo
                if detalle.articulo:
                    # Articulo tiene ManyToMany unidades_medida, obtener la primera o mostrar todas
                    unidades = detalle.articulo.unidades_medida.all()
                    if unidades.exists():
                        unidad = ', '.join([u.simbolo for u in unidades])
                    else:
                        unidad = 'unidad'
                else:
                    # Los activos son bienes únicos sin unidad de medida
                    unidad = 'unidad'

                self.fields[field_name] = forms.DecimalField(
                    label=f'Cantidad Despachada - {detalle.producto_nombre}',
                    max_digits=10,
                    decimal_places=2,
                    min_value=0,
                    max_value=max_cantidad,
                    initial=max_cantidad,
                    widget=forms.NumberInput(
                        attrs={
                            'class': 'form-control',
                            'step': '0.01'
                        }
                    ),
                    help_text=f'Aprobada: {detalle.cantidad_aprobada} {unidad}'
                )


class RechazarSolicitudForm(forms.Form):
    """Formulario para rechazar una solicitud"""

    motivo_rechazo = forms.CharField(
        label='Motivo del Rechazo',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describa el motivo del rechazo...'
            }
        ),
        required=True
    )


class FiltroSolicitudesForm(forms.Form):
    """Formulario para filtrar solicitudes en la lista"""

    estado = forms.ModelChoiceField(
        queryset=EstadoSolicitud.objects.filter(activo=True),
        required=False,
        empty_label='Todos los estados',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tipo = forms.ModelChoiceField(
        queryset=TipoSolicitud.objects.filter(activo=True),
        required=False,
        empty_label='Todos los tipos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    buscar = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Buscar por número, solicitante, área...'
            }
        )
    )
