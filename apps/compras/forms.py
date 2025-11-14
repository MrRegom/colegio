"""
Formularios para el módulo de compras.

Implementa validaciones personalizadas y limpieza de datos siguiendo
las mejores prácticas de Django 5.2.
"""
from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import (
    Proveedor, OrdenCompra, DetalleOrdenCompraArticulo, DetalleOrdenCompra,
    EstadoOrdenCompra, RecepcionArticulo, DetalleRecepcionArticulo,
    RecepcionActivo, DetalleRecepcionActivo, EstadoRecepcion, TipoRecepcion
)
from apps.bodega.models import Bodega, Articulo
from apps.activos.models import Activo


# ==================== FORMULARIOS DE PROVEEDOR ====================

class ProveedorForm(forms.ModelForm):
    """
    Formulario para crear/editar proveedores.

    Incluye validación de RUT único y formato de datos de contacto.
    """

    class Meta:
        model = Proveedor
        fields = [
            'rut', 'razon_social',
            'direccion', 'comuna', 'ciudad', 'telefono', 'email', 'sitio_web',
            'activo'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-select'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_rut(self) -> str:
        """Validar formato y unicidad del RUT."""
        rut = self.cleaned_data.get('rut', '').strip().upper()

        # Validar unicidad
        queryset = Proveedor.objects.filter(rut=rut, eliminado=False)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(f'Ya existe un proveedor con el RUT "{rut}".')

        return rut


# ==================== FORMULARIOS DE ORDEN DE COMPRA ====================

class OrdenCompraForm(forms.ModelForm):
    """Formulario para crear/editar órdenes de compra."""

    class Meta:
        model = OrdenCompra
        fields = [
            'fecha_orden', 'fecha_entrega_esperada',
            'proveedor', 'bodega_destino', 'estado', 'solicitudes', 'observaciones'
        ]
        widgets = {
            'fecha_orden': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_entrega_esperada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'bodega_destino': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'solicitudes': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5',
                'data-live-search': 'true'
            }),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar proveedores activos
        self.fields['proveedor'].queryset = Proveedor.objects.filter(
            activo=True, eliminado=False
        ).order_by('razon_social')

        # Filtrar bodegas activas
        self.fields['bodega_destino'].queryset = Bodega.objects.filter(
            activo=True, eliminado=False
        ).order_by('nombre')

        # Filtrar estados activos
        self.fields['estado'].queryset = EstadoOrdenCompra.objects.filter(
            activo=True
        ).order_by('codigo')

        # Filtrar solicitudes aprobadas (solo no eliminadas y con estado APROBADA)
        from apps.solicitudes.models import Solicitud
        self.fields['solicitudes'].queryset = Solicitud.objects.filter(
            estado__codigo='APROBADA',
            eliminado=False
        ).select_related('solicitante', 'estado').order_by('-numero')
        self.fields['solicitudes'].required = False
        self.fields['solicitudes'].help_text = 'Seleccione las solicitudes aprobadas asociadas a esta orden (opcional)'

        # Establecer estado inicial por defecto (primer estado activo)
        if not self.instance.pk:
            estado_inicial = EstadoOrdenCompra.objects.filter(
                activo=True
            ).order_by('codigo').first()
            if estado_inicial:
                self.fields['estado'].initial = estado_inicial

    def clean(self):
        """Validar fechas."""
        cleaned_data = super().clean()
        fecha_orden = cleaned_data.get('fecha_orden')
        fecha_entrega_esperada = cleaned_data.get('fecha_entrega_esperada')

        if fecha_orden and fecha_entrega_esperada:
            if fecha_entrega_esperada < fecha_orden:
                raise ValidationError({
                    'fecha_entrega_esperada': 'La fecha de entrega esperada no puede ser anterior a la fecha de orden.'
                })

        return cleaned_data


class DetalleOrdenCompraArticuloForm(forms.ModelForm):
    """Formulario para agregar artículos a una orden de compra."""

    class Meta:
        model = DetalleOrdenCompraArticulo
        fields = ['articulo', 'cantidad', 'precio_unitario', 'descuento', 'observaciones']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'value': '0'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].queryset = Articulo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria').order_by('codigo')

    def clean(self):
        """Validar que el descuento no sea mayor que el subtotal."""
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')
        descuento = cleaned_data.get('descuento', Decimal('0'))

        if cantidad and precio_unitario:
            subtotal_sin_descuento = cantidad * precio_unitario
            if descuento > subtotal_sin_descuento:
                raise ValidationError({
                    'descuento': f'El descuento no puede ser mayor que el subtotal (${subtotal_sin_descuento:,.2f}).'
                })

        return cleaned_data


class DetalleOrdenCompraActivoForm(forms.ModelForm):
    """Formulario para agregar activos a una orden de compra."""

    class Meta:
        model = DetalleOrdenCompra
        fields = ['activo', 'cantidad', 'precio_unitario', 'descuento', 'observaciones']
        widgets = {
            'activo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'value': '0'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].queryset = Activo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria').order_by('codigo')

    def clean(self):
        """Validar que el descuento no sea mayor que el subtotal."""
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')
        descuento = cleaned_data.get('descuento', Decimal('0'))

        if cantidad and precio_unitario:
            subtotal_sin_descuento = cantidad * precio_unitario
            if descuento > subtotal_sin_descuento:
                raise ValidationError({
                    'descuento': f'El descuento no puede ser mayor que el subtotal (${subtotal_sin_descuento:,.2f}).'
                })

        return cleaned_data


class OrdenCompraFiltroForm(forms.Form):
    """Formulario para filtrar órdenes de compra."""

    q = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por número...'
        })
    )

    estado = forms.ModelChoiceField(
        required=False,
        label='Estado',
        queryset=EstadoOrdenCompra.objects.filter(activo=True).order_by('nombre'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    proveedor = forms.ModelChoiceField(
        required=False,
        label='Proveedor',
        queryset=Proveedor.objects.filter(activo=True, eliminado=False).order_by('razon_social'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )


# ==================== FORMULARIOS DE RECEPCIÓN DE ARTÍCULOS ====================

class RecepcionArticuloForm(forms.ModelForm):
    """Formulario para crear/editar recepciones de artículos."""

    class Meta:
        model = RecepcionArticulo
        fields = ['tipo', 'orden_compra', 'bodega', 'documento_referencia', 'observaciones']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo'}),
            'orden_compra': forms.Select(attrs={'class': 'form-select', 'id': 'id_orden_compra'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'documento_referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guía/Factura'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar tipos de recepción activos
        self.fields['tipo'].queryset = TipoRecepcion.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

        # Filtrar todas las órdenes de compra disponibles
        # Excluir estados finales: RECIBIDA, CANCELADA, CERRADA
        self.fields['orden_compra'].queryset = OrdenCompra.objects.exclude(
            estado__codigo__in=['RECIBIDA', 'CANCELADA', 'CERRADA']
        ).select_related('proveedor', 'estado').order_by('-numero')
        self.fields['orden_compra'].required = False

        # Filtrar bodegas activas
        self.fields['bodega'].queryset = Bodega.objects.filter(
            activo=True, eliminado=False
        ).order_by('nombre')

    def clean(self):
        """Validar que si el tipo requiere orden de compra, se haya seleccionado una."""
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        orden_compra = cleaned_data.get('orden_compra')

        if tipo and tipo.requiere_orden and not orden_compra:
            raise ValidationError({
                'orden_compra': f'El tipo de recepción "{tipo.nombre}" requiere seleccionar una orden de compra.'
            })

        return cleaned_data


class DetalleRecepcionArticuloForm(forms.ModelForm):
    """Formulario para agregar artículos a una recepción."""

    class Meta:
        model = DetalleRecepcionArticulo
        fields = ['articulo', 'cantidad', 'lote', 'fecha_vencimiento', 'observaciones']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'lote': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].queryset = Articulo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria').order_by('codigo')
        self.fields['lote'].required = False
        self.fields['fecha_vencimiento'].required = False


class RecepcionArticuloFiltroForm(forms.Form):
    """Formulario para filtrar recepciones de artículos."""

    estado = forms.ModelChoiceField(
        required=False,
        label='Estado',
        queryset=EstadoRecepcion.objects.filter(activo=True, eliminado=False).order_by('nombre'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    bodega = forms.ModelChoiceField(
        required=False,
        label='Bodega',
        queryset=Bodega.objects.filter(activo=True, eliminado=False).order_by('nombre'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )


# ==================== FORMULARIOS DE RECEPCIÓN DE ACTIVOS ====================

class RecepcionActivoForm(forms.ModelForm):
    """
    Formulario para crear/editar recepciones de activos/bienes.

    Incluye funcionalidad completa: tipo de recepción, asociación con OC,
    y validaciones automáticas (similar a RecepcionArticuloForm).
    """

    class Meta:
        model = RecepcionActivo
        fields = ['tipo', 'orden_compra', 'documento_referencia', 'observaciones']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo'}),
            'orden_compra': forms.Select(attrs={'class': 'form-select', 'id': 'id_orden_compra'}),
            'documento_referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guía/Factura'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar tipos de recepción activos
        self.fields['tipo'].queryset = TipoRecepcion.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

        # Filtrar órdenes no finalizadas (excluir estados finales por codigo)
        self.fields['orden_compra'].queryset = OrdenCompra.objects.exclude(
            estado__codigo__in=['RECIBIDA', 'CANCELADA', 'CERRADA']
        ).select_related('proveedor', 'estado').order_by('-numero')
        self.fields['orden_compra'].required = False

    def clean(self):
        """Validar que si el tipo requiere orden de compra, se haya seleccionado una."""
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        orden_compra = cleaned_data.get('orden_compra')

        if tipo and tipo.requiere_orden and not orden_compra:
            raise ValidationError({
                'orden_compra': f'El tipo de recepción "{tipo.nombre}" requiere seleccionar una orden de compra.'
            })

        return cleaned_data


class DetalleRecepcionActivoForm(forms.ModelForm):
    """Formulario para agregar activos a una recepción."""

    class Meta:
        model = DetalleRecepcionActivo
        fields = ['activo', 'cantidad', 'numero_serie', 'observaciones']
        widgets = {
            'activo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activo'].queryset = Activo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria').order_by('codigo')
        self.fields['numero_serie'].required = False


class RecepcionActivoFiltroForm(forms.Form):
    """Formulario para filtrar recepciones de activos."""

    estado = forms.ModelChoiceField(
        required=False,
        label='Estado',
        queryset=EstadoRecepcion.objects.filter(activo=True, eliminado=False).order_by('nombre'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
