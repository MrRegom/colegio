"""
Formularios para el módulo de bodega.
Implementa validación centralizada siguiendo buenas prácticas Django.
"""
from django import forms
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .models import (
    Bodega, UnidadMedida, Categoria, Articulo, TipoMovimiento, Movimiento,
    TipoEntrega, EntregaArticulo, EntregaBien
)


# ==================== FORMULARIOS DE CONFIGURACIÓN ====================

class UnidadMedidaForm(forms.ModelForm):
    """
    Formulario para crear y editar unidades de medida.

    Este formulario pertenece al módulo de BODEGA, no al módulo de activos.
    """

    class Meta:
        model = UnidadMedida
        fields = ['codigo', 'nombre', 'simbolo', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de unidad (Ej: UN, KG, LT)',
                'maxlength': '10'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la unidad (Ej: Unidad, Kilogramo)'
            }),
            'simbolo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Símbolo (Ej: UN, kg, L)',
                'maxlength': '10'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'simbolo': 'Símbolo',
            'activo': 'Activo'
        }

    def clean_codigo(self):
        """Validar que el código sea único (en mayúsculas)."""
        codigo = self.cleaned_data.get('codigo', '').strip().upper()

        # Si estamos editando, excluir la instancia actual
        queryset = UnidadMedida.objects.filter(codigo=codigo)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                f'Ya existe una unidad de medida con el código "{codigo}".'
            )

        return codigo

    def clean_nombre(self):
        """Limpiar y validar el nombre."""
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre es obligatorio.')
        return nombre

    def clean_simbolo(self):
        """Limpiar y validar el símbolo."""
        simbolo = self.cleaned_data.get('simbolo', '').strip()
        if not simbolo:
            raise ValidationError('El símbolo es obligatorio.')
        return simbolo


class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar categorías de artículos."""

    class Meta:
        model = Categoria
        fields = ['codigo', 'nombre', 'descripcion', 'observaciones', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de categoría',
                'maxlength': '20'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la categoría',
                'rows': 3
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales',
                'rows': 2
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'observaciones': 'Observaciones',
            'activo': 'Activo'
        }

    def clean_codigo(self):
        """Validar que el código sea único (en mayúsculas)."""
        codigo = self.cleaned_data.get('codigo', '').strip().upper()

        # Si estamos editando, excluir la instancia actual
        queryset = Categoria.objects.filter(codigo=codigo)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                f'Ya existe una categoría con el código "{codigo}".'
            )

        return codigo

    def clean_nombre(self):
        """Limpiar y validar el nombre."""
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre es obligatorio.')
        return nombre


class ArticuloForm(forms.ModelForm):
    """
    Formulario para crear y editar artículos de bodega.

    Permite seleccionar una marca y una unidad de medida a la vez,
    que se agregarán a las relaciones ManyToMany del artículo.
    """
    # Campos personalizados para selección simple
    marca_seleccionada = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Marca',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Seleccione una marca para agregar al artículo'
    )

    unidad_seleccionada = forms.ModelChoiceField(
        queryset=None,
        required=True,
        label='Unidad de Medida',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Seleccione una unidad de medida para agregar al artículo'
    )

    class Meta:
        model = Articulo
        fields = [
            'codigo', 'nombre', 'descripcion', 'categoria',
            'stock_actual', 'stock_minimo', 'stock_maximo', 'punto_reorden',
            'ubicacion_fisica', 'observaciones', 'activo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del artículo',
                'required': True
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del artículo',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada',
                'rows': 3
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'readonly': True,
                'disabled': True
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'stock_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional',
                'step': '0.01',
                'min': '0'
            }),
            'punto_reorden': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional',
                'step': '0.01',
                'min': '0'
            }),
            'ubicacion_fisica': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales',
                'rows': 2
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar solo categorías activas y no eliminadas
        self.fields['categoria'].queryset = Categoria.objects.filter(
            activo=True,
            eliminado=False
        ).order_by('codigo')

        # Filtrar solo bodegas activas y no eliminadas
        self.fields['ubicacion_fisica'].queryset = Bodega.objects.filter(
            activo=True,
            eliminado=False
        ).order_by('codigo')

        # Configurar queryset para marca_seleccionada
        from apps.activos.models import Marca
        self.fields['marca_seleccionada'].queryset = Marca.objects.filter(
            activo=True,
            eliminado=False
        ).order_by('nombre')
        self.fields['marca_seleccionada'].empty_label = 'Seleccione una marca (opcional)'

        # Configurar queryset para unidad_seleccionada
        self.fields['unidad_seleccionada'].queryset = UnidadMedida.objects.filter(
            activo=True,
            eliminado=False
        ).order_by('codigo')
        self.fields['unidad_seleccionada'].empty_label = 'Seleccione una unidad de medida'

        # Hacer el campo stock_actual de solo lectura
        self.fields['stock_actual'].disabled = True
        self.fields['stock_actual'].required = False

        # Si estamos editando (instance existe), hacer el código readonly
        if self.instance and self.instance.pk:
            self.fields['codigo'].disabled = True
            self.fields['codigo'].widget.attrs['readonly'] = True
            self.fields['codigo'].help_text = 'El código no puede modificarse al editar'
            # En edición, marca y unidad son opcionales (solo para agregar nuevas)
            self.fields['unidad_seleccionada'].required = False
            self.fields['unidad_seleccionada'].help_text = 'Seleccione una unidad adicional (opcional)'

    def save(self, commit=True):
        """
        Guardar el artículo y agregar la marca y unidad seleccionadas
        a las relaciones ManyToMany.
        """
        instance = super().save(commit=False)

        if commit:
            # Primero guardar la instancia
            instance.save()

            # Luego guardar las relaciones M2M existentes
            self.save_m2m()

            # Agregar marca seleccionada a la relación M2M (si se seleccionó)
            marca = self.cleaned_data.get('marca_seleccionada')
            if marca:
                if not instance.marcas.filter(pk=marca.pk).exists():
                    instance.marcas.add(marca)

            # Agregar unidad seleccionada a la relación M2M (si se seleccionó)
            unidad = self.cleaned_data.get('unidad_seleccionada')
            if unidad:
                if not instance.unidades_medida.filter(pk=unidad.pk).exists():
                    instance.unidades_medida.add(unidad)

        return instance

    def clean_codigo(self):
        """Validar que el código sea único (en mayúsculas)."""
        codigo = self.cleaned_data.get('codigo', '').strip().upper()

        # Si estamos editando, excluir la instancia actual
        queryset = Articulo.objects.filter(codigo=codigo)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError(
                f'Ya existe un artículo con el código "{codigo}".'
            )

        return codigo

    def clean_stock_minimo(self):
        """Validar que el stock mínimo no sea negativo."""
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo and stock_minimo < 0:
            raise ValidationError('El stock mínimo no puede ser negativo.')
        return stock_minimo

    def clean_stock_maximo(self):
        """Validar que el stock máximo no sea negativo."""
        stock_maximo = self.cleaned_data.get('stock_maximo')
        if stock_maximo and stock_maximo < 0:
            raise ValidationError('El stock máximo no puede ser negativo.')
        return stock_maximo

    def clean_punto_reorden(self):
        """Validar que el punto de reorden no sea negativo."""
        punto_reorden = self.cleaned_data.get('punto_reorden')
        if punto_reorden and punto_reorden < 0:
            raise ValidationError('El punto de reorden no puede ser negativo.')
        return punto_reorden

    def clean(self):
        """Validaciones de múltiples campos."""
        cleaned_data = super().clean()
        stock_minimo = cleaned_data.get('stock_minimo')
        stock_maximo = cleaned_data.get('stock_maximo')
        punto_reorden = cleaned_data.get('punto_reorden')

        # Validar que stock máximo sea mayor que mínimo
        if stock_minimo and stock_maximo:
            if stock_maximo <= stock_minimo:
                raise ValidationError({
                    'stock_maximo': 'El stock máximo debe ser mayor que el stock mínimo.'
                })

        # Validar que punto de reorden esté entre mínimo y máximo
        if punto_reorden and stock_minimo:
            if punto_reorden < stock_minimo:
                raise ValidationError({
                    'punto_reorden': 'El punto de reorden debe ser mayor o igual al stock mínimo.'
                })

        return cleaned_data


class MovimientoForm(forms.ModelForm):
    """Formulario para registrar movimientos de inventario."""

    class Meta:
        model = Movimiento
        fields = ['articulo', 'tipo', 'cantidad', 'operacion', 'motivo']
        widgets = {
            'articulo': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'id_articulo'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'operacion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa el motivo del movimiento',
                'rows': 3,
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo artículos activos y no eliminados
        self.fields['articulo'].queryset = Articulo.objects.filter(
            activo=True,
            eliminado=False
        ).select_related('categoria').order_by('codigo')

        # Filtrar solo tipos de movimiento activos
        self.fields['tipo'].queryset = TipoMovimiento.objects.filter(
            activo=True,
            eliminado=False
        ).order_by('codigo')

    def clean_cantidad(self):
        """Validar que la cantidad sea positiva."""
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad and cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a cero.')
        return cantidad

    def clean(self):
        """Validar que haya suficiente stock para salidas."""
        cleaned_data = super().clean()
        articulo = cleaned_data.get('articulo')
        cantidad = cleaned_data.get('cantidad')
        operacion = cleaned_data.get('operacion')

        # Validar stock disponible para salidas
        if articulo and cantidad and operacion == 'SALIDA':
            if articulo.stock_actual < cantidad:
                # Obtener unidades de medida
                unidades = articulo.unidades_medida.all()
                if unidades.exists():
                    unidades_str = ', '.join([u.simbolo for u in unidades])
                else:
                    unidades_str = 'unidad'
                raise ValidationError({
                    'cantidad': f'Stock insuficiente. Disponible: {articulo.stock_actual} {unidades_str}'
                })

        return cleaned_data


class ArticuloFiltroForm(forms.Form):
    """Formulario para filtrar artículos."""

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por código, nombre o marca...'
        }),
        label='Búsqueda'
    )

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activo=True, eliminado=False),
        required=False,
        empty_label='Todas las categorías',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Categoría'
    )

    bodega = forms.ModelChoiceField(
        queryset=Bodega.objects.filter(activo=True, eliminado=False),
        required=False,
        empty_label='Todas las bodegas',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Bodega'
    )

    activo = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Todos'),
            ('1', 'Activos'),
            ('0', 'Inactivos')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Estado'
    )


# ==================== FORMULARIOS DE ENTREGA ====================

class EntregaArticuloForm(forms.ModelForm):
    """Formulario para crear entregas de artículos."""

    class Meta:
        model = EntregaArticulo
        fields = [
            'solicitud', 'bodega_origen', 'tipo', 'recibido_por',
            'departamento_destino', 'motivo', 'observaciones'
        ]
        widgets = {
            'solicitud': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_solicitud'
            }),
            'bodega_origen': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'recibido_por': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'departamento_destino': forms.Select(attrs={
                'class': 'form-select'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa el motivo de la entrega',
                'rows': 3,
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales (opcional)',
                'rows': 2
            })
        }
        labels = {
            'solicitud': 'Solicitud Asociada (Opcional)',
            'bodega_origen': 'Bodega de Origen',
            'tipo': 'Tipo de Entrega',
            'recibido_por': 'Recibido Por (Usuario)',
            'departamento_destino': 'Departamento Destino',
            'motivo': 'Motivo',
            'observaciones': 'Observaciones'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar TODAS las solicitudes de artículos (sin importar el estado)
        from apps.solicitudes.models import Solicitud
        try:
            self.fields['solicitud'].queryset = Solicitud.objects.filter(
                tipo='ARTICULO',
                eliminado=False
            ).select_related('estado', 'solicitante').order_by('-numero')
            self.fields['solicitud'].empty_label = 'Seleccione solicitud (opcional)'
            # Personalizar cómo se muestra cada solicitud en el dropdown
            self.fields['solicitud'].label_from_instance = lambda obj: f"{obj.numero} - {obj.estado.nombre} - {obj.solicitante.get_full_name() or obj.solicitante.username}"
        except:
            self.fields['solicitud'].queryset = Solicitud.objects.none()
            self.fields['solicitud'].empty_label = 'No hay solicitudes disponibles'

        # Filtrar solo bodegas y tipos activos
        self.fields['bodega_origen'].queryset = Bodega.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

        self.fields['tipo'].queryset = TipoEntrega.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

        # Filtrar usuarios activos
        from django.contrib.auth.models import User
        self.fields['recibido_por'].queryset = User.objects.filter(
            is_active=True
        ).order_by('first_name', 'last_name')

        # Filtrar departamentos activos
        from apps.solicitudes.models import Departamento
        self.fields['departamento_destino'].queryset = Departamento.objects.filter(
            activo=True, eliminado=False
        ).order_by('nombre')
        self.fields['departamento_destino'].empty_label = 'Seleccione departamento (opcional)'

    def clean_motivo(self):
        """Validar que el motivo no esté vacío."""
        motivo = self.cleaned_data.get('motivo', '').strip()
        if not motivo:
            raise ValidationError('El motivo de la entrega es obligatorio.')
        return motivo


class EntregaBienForm(forms.ModelForm):
    """Formulario para crear entregas de bienes/activos."""

    class Meta:
        model = EntregaBien
        fields = [
            'tipo', 'recibido_por',
            'departamento_destino', 'motivo', 'observaciones'
        ]
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'recibido_por': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'departamento_destino': forms.Select(attrs={
                'class': 'form-select'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa el motivo de la entrega',
                'rows': 3,
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales (opcional)',
                'rows': 2
            })
        }
        labels = {
            'tipo': 'Tipo de Entrega',
            'recibido_por': 'Recibido Por (Usuario)',
            'departamento_destino': 'Departamento Destino',
            'motivo': 'Motivo',
            'observaciones': 'Observaciones'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo tipos activos
        self.fields['tipo'].queryset = TipoEntrega.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

        # Filtrar usuarios activos
        from django.contrib.auth.models import User
        self.fields['recibido_por'].queryset = User.objects.filter(
            is_active=True
        ).order_by('first_name', 'last_name')

        # Filtrar departamentos activos
        from apps.solicitudes.models import Departamento
        self.fields['departamento_destino'].queryset = Departamento.objects.filter(
            activo=True, eliminado=False
        ).order_by('nombre')
        self.fields['departamento_destino'].empty_label = 'Seleccione departamento (opcional)'

    def clean_motivo(self):
        """Validar que el motivo no esté vacío."""
        motivo = self.cleaned_data.get('motivo', '').strip()
        if not motivo:
            raise ValidationError('El motivo de la entrega es obligatorio.')
        return motivo