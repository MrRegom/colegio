from decimal import Decimal
from typing import Any

from django.contrib.auth.models import User
from django.core.validators import EmailValidator, MinValueValidator
from django.db import models

from apps.activos.models import Activo
from apps.bodega.models import Articulo, Bodega
from core.models import BaseModel


class Proveedor(BaseModel):
    """
    Modelo para gestionar proveedores del sistema de compras.

    Almacena información completa de proveedores incluyendo datos de contacto
    y condiciones comerciales.
    """

    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    razon_social = models.CharField(max_length=255, verbose_name='Razón Social')

    # Contacto
    direccion = models.CharField(max_length=255, verbose_name='Dirección')
    comuna = models.CharField(max_length=100, blank=True, null=True, verbose_name='Comuna')
    ciudad = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ciudad')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    email = models.EmailField(
        validators=[EmailValidator()],
        blank=True,
        null=True,
        verbose_name='Correo Electrónico'
    )
    sitio_web = models.URLField(blank=True, null=True, verbose_name='Sitio Web')

    class Meta:
        db_table = 'tba_compras_proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['razon_social']

    def __str__(self) -> str:
        return f"{self.rut} - {self.razon_social}"


class EstadoOrdenCompra(BaseModel):
    """
    Catálogo de estados de órdenes de compra.

    Define los diferentes estados que puede tener una orden de compra
    durante su ciclo de vida (ej: PENDIENTE, APROBADA, RECIBIDA).
    """

    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    color = models.CharField(
        max_length=7,
        default='#6c757d',
        verbose_name='Color (Hex)'
    )

    class Meta:
        db_table = 'tba_compras_conf_estado_orden'
        verbose_name = 'Estado de Orden de Compra'
        verbose_name_plural = 'Estados de Órdenes de Compra'
        ordering = ['codigo']

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"


class OrdenCompra(BaseModel):
    """
    Modelo para gestionar órdenes de compra.

    Representa una orden de compra emitida a un proveedor, incluyendo
    información de fechas, montos, estado y relaciones con solicitudes.
    """

    numero = models.CharField(max_length=20, unique=True, verbose_name='Número de Orden')
    fecha_orden = models.DateField(verbose_name='Fecha de Orden')
    fecha_entrega_esperada = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha Entrega Esperada'
    )
    fecha_entrega_real = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha Entrega Real'
    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='ordenes_compra',
        verbose_name='Proveedor'
    )
    bodega_destino = models.ForeignKey(
        Bodega,
        on_delete=models.PROTECT,
        related_name='ordenes_compra',
        verbose_name='Bodega Destino'
    )
    estado = models.ForeignKey(
        EstadoOrdenCompra,
        on_delete=models.PROTECT,
        related_name='ordenes_compra',
        verbose_name='Estado'
    )
    solicitante = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ordenes_solicitadas',
        verbose_name='Solicitante'
    )
    aprobador = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ordenes_aprobadas',
        verbose_name='Aprobador',
        blank=True,
        null=True
    )

    # Relación con solicitudes aprobadas
    solicitudes = models.ManyToManyField(
        'solicitudes.Solicitud',
        related_name='ordenes_compra',
        blank=True,
        verbose_name='Solicitudes Asociadas',
        help_text='Solicitudes aprobadas que originan esta orden de compra'
    )

    # Montos
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Subtotal'
    )
    impuesto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Impuesto (IVA)'
    )
    descuento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Descuento'
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Total'
    )

    # Observaciones
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        db_table = 'tba_compras_orden'
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
        ordering = ['-fecha_orden', '-numero']

    def __str__(self) -> str:
        return f"OC-{self.numero} - {self.proveedor.razon_social}"


class DetalleOrdenCompra(BaseModel):
    """
    Modelo para el detalle de activos en una orden de compra.

    Representa cada línea de activos incluidos en una orden de compra,
    con información de cantidad, precios y seguimiento de recepción.
    """

    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Orden de Compra'
    )
    activo = models.ForeignKey(
        Activo,
        on_delete=models.PROTECT,
        related_name='detalles_compra',
        verbose_name='Activo'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Cantidad'
    )
    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Precio Unitario'
    )
    descuento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Descuento'
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Subtotal'
    )
    cantidad_recibida = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Cantidad Recibida'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        db_table = 'tba_compras_orden_detalle'
        verbose_name = 'Detalle de Orden de Compra'
        verbose_name_plural = 'Detalles de Órdenes de Compra'
        ordering = ['orden_compra', 'id']

    def __str__(self) -> str:
        return f"{self.orden_compra.numero} - {self.activo.codigo} ({self.cantidad})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Calcula el subtotal automáticamente antes de guardar."""
        precio = self.precio_unitario or Decimal('0')
        descuento = self.descuento or Decimal('0')
        self.subtotal = (self.cantidad * precio) - descuento
        super().save(*args, **kwargs)


class DetalleOrdenCompraArticulo(BaseModel):
    """
    Modelo para el detalle de artículos de bodega en una orden de compra.

    Representa cada línea de artículos de bodega incluidos en una orden de compra,
    con información de cantidad, precios y seguimiento de recepción.
    """

    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name='detalles_articulos',
        verbose_name='Orden de Compra'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name='detalles_compra',
        verbose_name='Artículo'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Cantidad'
    )
    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Precio Unitario'
    )
    descuento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Descuento'
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Subtotal'
    )
    cantidad_recibida = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Cantidad Recibida'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        db_table = 'tba_compras_orden_detalle_articulo'
        verbose_name = 'Detalle Orden - Artículo'
        verbose_name_plural = 'Detalles Orden - Artículos'
        ordering = ['orden_compra', 'id']

    def __str__(self) -> str:
        return f"{self.orden_compra.numero} - {self.articulo.codigo} ({self.cantidad})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Calcula el subtotal automáticamente antes de guardar."""
        precio = self.precio_unitario or Decimal('0')
        descuento = self.descuento or Decimal('0')
        self.subtotal = (self.cantidad * precio) - descuento
        super().save(*args, **kwargs)


# ==================== RECEPCIÓN DE ARTÍCULOS ====================

class RecepcionBase(BaseModel):
    """
    Modelo base abstracto para recepciones (artículos y activos).

    Contiene todos los campos comunes a ambos tipos de recepción.
    Principio DRY: Evita duplicación de código entre RecepcionArticulo y RecepcionActivo.

    Este modelo no crea tabla en la base de datos (abstract=True).
    """

    numero = models.CharField(max_length=30, unique=True, verbose_name='Número de Recepción')
    fecha_recepcion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Recepción')
    tipo = models.ForeignKey(
        'TipoRecepcion',
        on_delete=models.PROTECT,
        related_name='%(class)s_set',  # Nombre dinámico según clase hija
        verbose_name='Tipo de Recepción',
        null=True,
        blank=True
    )
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.PROTECT,
        related_name='%(class)s_set',
        verbose_name='Orden de Compra',
        blank=True,
        null=True
    )
    estado = models.ForeignKey(
        'EstadoRecepcion',
        on_delete=models.PROTECT,
        related_name='%(class)s_set',
        verbose_name='Estado'
    )
    recibido_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_recibidas',
        verbose_name='Recibido Por'
    )
    documento_referencia = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Documento Referencia (Guía/Factura)'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        abstract = True  # Modelo abstracto, no crea tabla en BD

    def __str__(self) -> str:
        return f"{self.numero} - {self.fecha_recepcion.strftime('%d/%m/%Y')}"


class DetalleRecepcionBase(BaseModel):
    """
    Modelo base abstracto para detalles de recepción.

    Contiene campos comunes a todos los detalles de recepción.
    Principio DRY: Evita duplicación entre DetalleRecepcionArticulo y DetalleRecepcionActivo.

    Este modelo no crea tabla en la base de datos (abstract=True).
    """

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Cantidad Recibida'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.cantidad} unidades"


class EstadoRecepcion(BaseModel):
    """
    Catálogo de estados de recepción.

    Define los diferentes estados que puede tener una recepción de artículos
    o activos (ej: PENDIENTE, COMPLETADA, CANCELADA).
    """

    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    color = models.CharField(max_length=7, default='#6c757d', verbose_name='Color (Hex)')

    class Meta:
        db_table = 'tba_compras_conf_estado_recepcion'
        verbose_name = 'Estado de Recepción'
        verbose_name_plural = 'Estados de Recepción'
        ordering = ['codigo']

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"


class TipoRecepcion(BaseModel):
    """
    Catálogo de tipos de recepción.

    Define los diferentes tipos de recepción que se pueden realizar
    (ej: CON_OC, SIN_OC, DONACION, DEVOLUCION).
    """

    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    requiere_orden = models.BooleanField(default=False, verbose_name='Requiere Orden de Compra')

    class Meta:
        db_table = 'tba_compras_conf_tipo_recepcion'
        verbose_name = 'Tipo de Recepción'
        verbose_name_plural = 'Tipos de Recepción'
        ordering = ['codigo']

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"


class RecepcionArticulo(RecepcionBase):
    """
    Modelo para gestionar recepciones de artículos de bodega.

    Hereda de RecepcionBase (DRY) y agrega solo el campo específico 'bodega'.
    Permite registrar la entrada de artículos a una bodega específica.
    """

    bodega = models.ForeignKey(
        Bodega,
        on_delete=models.PROTECT,
        related_name='recepciones_articulos',
        verbose_name='Bodega'
    )

    class Meta:
        db_table = 'tba_compras_recepcion_articulo'
        verbose_name = 'Recepción de Artículo'
        verbose_name_plural = 'Recepciones de Artículos'
        ordering = ['-fecha_recepcion']

    def __str__(self) -> str:
        return f"REC-ART-{self.numero} - {self.fecha_recepcion.strftime('%d/%m/%Y')}"


class DetalleRecepcionArticulo(DetalleRecepcionBase):
    """
    Detalle de artículos recibidos.

    Hereda de DetalleRecepcionBase (DRY) y agrega campos específicos de artículos
    como lote y fecha de vencimiento.
    """

    recepcion = models.ForeignKey(
        RecepcionArticulo,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Recepción'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name='recepciones',
        verbose_name='Artículo'
    )
    # Campos específicos de artículos (no se encuentran en activos)
    lote = models.CharField(max_length=50, blank=True, null=True, verbose_name='Lote')
    fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name='Fecha de Vencimiento')

    class Meta:
        db_table = 'tba_compras_recepcion_articulo_detalle'
        verbose_name = 'Detalle Recepción Artículo'
        verbose_name_plural = 'Detalles Recepción Artículos'
        ordering = ['recepcion', 'id']

    def __str__(self) -> str:
        return f"{self.recepcion.numero} - {self.articulo.codigo} ({self.cantidad})"


# ==================== RECEPCIÓN DE BIENES (ACTIVOS) ====================

class RecepcionActivo(RecepcionBase):
    """
    Modelo para gestionar recepciones de bienes/activos fijos.

    Hereda de RecepcionBase (DRY) sin agregar campos adicionales.
    Diferencia con RecepcionArticulo: No requiere bodega ya que los activos
    fijos no se almacenan en bodegas.
    """

    class Meta:
        db_table = 'tba_compras_recepcion_activo'
        verbose_name = 'Recepción de Bien/Activo'
        verbose_name_plural = 'Recepciones de Bienes/Activos'
        ordering = ['-fecha_recepcion']

    def __str__(self) -> str:
        return f"REC-ACT-{self.numero} - {self.fecha_recepcion.strftime('%d/%m/%Y')}"


class DetalleRecepcionActivo(DetalleRecepcionBase):
    """
    Detalle de activos/bienes recibidos.

    Hereda de DetalleRecepcionBase (DRY) y agrega campos específicos de activos
    como número de serie para identificación individual.
    """

    recepcion = models.ForeignKey(
        RecepcionActivo,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Recepción'
    )
    activo = models.ForeignKey(
        Activo,
        on_delete=models.PROTECT,
        related_name='recepciones',
        verbose_name='Activo/Bien'
    )
    # Campo específico de activos (no se encuentra en artículos)
    numero_serie = models.CharField(max_length=100, blank=True, null=True, verbose_name='Número de Serie')

    class Meta:
        db_table = 'tba_compras_recepcion_activo_detalle'
        verbose_name = 'Detalle Recepción Activo'
        verbose_name_plural = 'Detalles Recepción Activos'
        ordering = ['recepcion', 'id']

    def __str__(self) -> str:
        return f"{self.recepcion.numero} - {self.activo.codigo} ({self.cantidad})"
