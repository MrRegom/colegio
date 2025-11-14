"""
Modelos del módulo de bodega.

Este módulo gestiona el inventario de artículos, movimientos, entregas y bodegas.
Todos los modelos heredan de BaseModel para tener soft delete y auditoría automática.

Convención de nomenclatura:
- Todas las tablas usan prefijo 'tba_bodega_'
- Se sigue nomenclatura Pascal Case para clases
- Se usan type hints en métodos __str__
"""
from typing import Optional
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from core.models import BaseModel


class Bodega(BaseModel):
    """Modelo para gestionar las bodegas del sistema"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    responsable = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bodegas_responsable',
        verbose_name='Responsable'
    )

    class Meta:
        db_table = 'tba_bodega_conf_bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en cadena de la bodega."""
        return f"{self.codigo} - {self.nombre}"

class UnidadMedida(BaseModel):
    """
    Catálogo de unidades de medida para artículos de bodega.

    Este modelo pertenece al módulo de BODEGA, no al módulo de activos.
    Se utiliza para definir las unidades de medida de los artículos (Unidad, Kilogramo, Litro, etc.).

    Hereda de BaseModel para soft delete y auditoría.
    """
    codigo = models.CharField(max_length=10, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    simbolo = models.CharField(max_length=10, verbose_name='Símbolo')

    class Meta:
        db_table = 'tba_bodega_unidad_medida'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en cadena de la unidad de medida."""
        return f"{self.codigo} - {self.nombre} ({self.simbolo})"

class Categoria(BaseModel):
    """Modelo para gestionar categorías de artículos"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        db_table = 'tba_bodega_conf_categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en cadena de la categoría."""
        return f"{self.codigo} - {self.nombre}"


class Articulo(BaseModel):
    """
    Modelo para gestionar artículos en bodega.

    Este modelo representa los artículos almacenados en las bodegas del sistema.
    Incluye control de stock, relaciones many-to-many con marcas y unidades de medida,
    y generación automática de códigos de barras.

    Attributes:
        codigo: Código único del artículo.
        nombre: Nombre descriptivo del artículo.
        descripcion: Descripción detallada opcional.
        marcas: Marcas asociadas al artículo (ManyToMany).
        codigo_barras: Código de barras (auto-generado si no se proporciona).
        categoria: Categoría a la que pertenece el artículo.
        stock_actual: Stock actual en bodega.
        stock_minimo: Stock mínimo requerido.
        stock_maximo: Stock máximo permitido (opcional).
        punto_reorden: Punto de reorden para alertas (opcional).
        unidades_medida: Unidades de medida aplicables al artículo (ManyToMany).
        ubicacion_fisica: Bodega donde se almacena el artículo.
        observaciones: Observaciones adicionales.
    """
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    marcas = models.ManyToManyField(
        'activos.Marca',
        related_name='articulos',
        blank=True,
        verbose_name='Marcas',
        help_text='Marcas asociadas al artículo'
    )
    codigo_barras = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Código de Barras',
        help_text='Código de barras del producto (dejar vacío para auto-generar)'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='articulos',
        verbose_name='Categoría'
    )
    stock_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock Actual'
    )
    stock_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock Mínimo'
    )
    stock_maximo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name='Stock Máximo'
    )
    punto_reorden = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name='Punto de Reorden'
    )
    unidades_medida = models.ManyToManyField(
        UnidadMedida,
        related_name='articulos',
        verbose_name='Unidades de Medida',
        help_text='Unidades de medida aplicables al artículo'
    )
    ubicacion_fisica = models.ForeignKey(
        Bodega,
        on_delete=models.PROTECT,
        related_name='articulos',
        verbose_name='Ubicación Física (Bodega)'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        db_table = 'tba_bodega_articulos'
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en cadena del artículo."""
        return f"{self.codigo} - {self.nombre}"

    def save(self, *args, **kwargs) -> None:
        """
        Guarda el artículo y auto-genera código de barras si no se proporciona.

        Si el código de barras no está definido, genera uno automáticamente
        basado en el código del artículo (limitado a 12 caracteres).
        """
        if not self.codigo_barras and self.codigo:
            # Generar código de barras desde el código
            self.codigo_barras = f"COD{self.codigo.replace('-', '').replace('_', '').upper()[:12]}"
        super().save(*args, **kwargs)


class TipoMovimiento(BaseModel):
    """Catálogo de tipos de movimiento de inventario"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tba_bodega_conf_tipomovimiento'
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimiento'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en cadena del tipo de movimiento."""
        return f"{self.codigo} - {self.nombre}"


class Movimiento(BaseModel):
    """Modelo para registrar movimientos de inventario"""
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name='movimientos',
        verbose_name='Artículo'
    )
    tipo = models.ForeignKey(
        TipoMovimiento,
        on_delete=models.PROTECT,
        related_name='movimientos',
        verbose_name='Tipo de Movimiento'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Cantidad'
    )
    operacion = models.CharField(
        max_length=20,
        choices=[
            ('ENTRADA', 'Entrada'),
            ('SALIDA', 'Salida'),
        ],
        verbose_name='Operación'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='movimientos_bodega',
        verbose_name='Usuario'
    )
    motivo = models.TextField(verbose_name='Motivo')
    stock_antes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Stock Antes'
    )
    stock_despues = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Stock Después'
    )

    class Meta:
        db_table = 'tba_bodega_movimientos'
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha_creacion']

    def __str__(self) -> str:
        """Representación en cadena del movimiento."""
        return f"{self.operacion} - {self.articulo.codigo} - {self.cantidad}"


# ==================== ENTREGA DE ARTÍCULOS Y BIENES ====================

class EntregaBase(BaseModel):
    """
    Modelo base abstracto para entregas (artículos y bienes).
    Contiene todos los campos comunes a ambos tipos de entrega.

    Principio DRY: Evita duplicación de código entre EntregaArticulo y EntregaBien.
    """
    numero = models.CharField(max_length=30, unique=True, verbose_name='Número de Entrega')
    fecha_entrega = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Entrega')
    tipo = models.ForeignKey(
        'TipoEntrega',
        on_delete=models.PROTECT,
        related_name='%(class)s_set',  # Nombre dinámico según clase hija
        verbose_name='Tipo de Entrega'
    )
    estado = models.ForeignKey(
        'EstadoEntrega',
        on_delete=models.PROTECT,
        related_name='%(class)s_set',
        verbose_name='Estado'
    )
    entregado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_entregadas_por',
        verbose_name='Entregado Por'
    )
    recibido_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_recibidas_por',
        verbose_name='Recibido Por',
        help_text='Usuario que recibe la entrega'
    )
    departamento_destino = models.ForeignKey(
        'solicitudes.Departamento',
        on_delete=models.PROTECT,
        related_name='%(class)s_entregas',
        blank=True,
        null=True,
        verbose_name='Departamento Destino'
    )
    motivo = models.TextField(verbose_name='Motivo de la Entrega')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        abstract = True  # Modelo abstracto, no crea tabla en BD

    def __str__(self) -> str:
        """Representación en cadena de la entrega."""
        return f"{self.numero} - {self.fecha_entrega.strftime('%d/%m/%Y')}"


class DetalleEntregaBase(BaseModel):
    """
    Modelo base abstracto para detalles de entrega.
    Contiene campos comunes a todos los detalles de entrega.

    Principio DRY: Evita duplicación entre DetalleEntregaArticulo y DetalleEntregaBien.
    """
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Cantidad Entregada'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Representación en cadena del detalle de entrega."""
        return f"{self.cantidad} unidades"


class EstadoEntrega(BaseModel):
    """Catálogo de estados de entrega"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    color = models.CharField(max_length=7, default='#6c757d', verbose_name='Color (Hex)')
    es_inicial = models.BooleanField(default=False, verbose_name='Estado Inicial')
    es_final = models.BooleanField(default=False, verbose_name='Estado Final')

    class Meta:
        db_table = 'tba_bodega_estado_entrega'
        verbose_name = 'Estado de Entrega'
        verbose_name_plural = 'Estados de Entrega'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en cadena del estado de entrega."""
        return f"{self.codigo} - {self.nombre}"


class TipoEntrega(BaseModel):
    """Catálogo de tipos de entrega"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    requiere_autorizacion = models.BooleanField(default=False, verbose_name='Requiere Autorización')

    class Meta:
        db_table = 'tba_bodega_conf_tipoentrega'
        verbose_name = 'Tipo de Entrega'
        verbose_name_plural = 'Tipos de Entrega'
        ordering = ['codigo']

    def __str__(self) -> str:
        """Representación en cadena del tipo de entrega."""
        return f"{self.codigo} - {self.nombre}"


class EntregaArticulo(EntregaBase):
    """
    Modelo para gestionar entregas de artículos de bodega.
    Hereda de EntregaBase (DRY) y agrega el campo específico 'bodega_origen'.

    Puede estar vinculada opcionalmente a una Solicitud de artículos,
    permitiendo entregas totales o parciales de la solicitud.
    """
    bodega_origen = models.ForeignKey(
        Bodega,
        on_delete=models.PROTECT,
        related_name='entregas_articulos',
        verbose_name='Bodega de Origen'
    )
    solicitud = models.ForeignKey(
        'solicitudes.Solicitud',
        on_delete=models.PROTECT,
        related_name='entregas_articulos',
        blank=True,
        null=True,
        verbose_name='Solicitud Asociada',
        help_text='Solicitud de artículos asociada a esta entrega (opcional)'
    )

    class Meta:
        db_table = 'tba_bodega_entrega_articulo'
        verbose_name = 'Entrega de Artículo'
        verbose_name_plural = 'Entregas de Artículos'
        ordering = ['-fecha_entrega']

    def __str__(self) -> str:
        """Representación en cadena de la entrega de artículo."""
        return f"ENT-ART-{self.numero} - {self.fecha_entrega.strftime('%d/%m/%Y')}"


class DetalleEntregaArticulo(DetalleEntregaBase):
    """
    Detalle de artículos entregados.
    Hereda de DetalleEntregaBase (DRY) y agrega campos específicos de artículos.

    Puede estar vinculado a un DetalleSolicitud para rastrear el despacho
    de solicitudes específicas.
    """
    entrega = models.ForeignKey(
        EntregaArticulo,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Entrega'
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name='entregas',
        verbose_name='Artículo'
    )
    lote = models.CharField(max_length=50, blank=True, null=True, verbose_name='Lote')
    detalle_solicitud = models.ForeignKey(
        'solicitudes.DetalleSolicitud',
        on_delete=models.PROTECT,
        related_name='detalles_entregas',
        blank=True,
        null=True,
        verbose_name='Detalle de Solicitud',
        help_text='Vincula con línea específica de solicitud (opcional)'
    )

    class Meta:
        db_table = 'tba_bodega_entrega_articulo_detalle'
        verbose_name = 'Detalle Entrega Artículo'
        verbose_name_plural = 'Detalles Entrega Artículos'
        ordering = ['entrega', 'id']

    def __str__(self) -> str:
        """Representación en cadena del detalle de entrega de artículo."""
        return f"{self.entrega.numero} - {self.articulo.codigo} ({self.cantidad})"


# ==================== ENTREGA DE BIENES (ACTIVOS) ====================

class EntregaBien(EntregaBase):
    """
    Modelo para gestionar entregas de bienes/activos fijos.
    Hereda de EntregaBase (DRY) sin agregar campos adicionales.

    Diferencia con EntregaArticulo: No requiere bodega de origen.
    Los bienes pueden ser activos que no están en bodega.
    """
    class Meta:
        db_table = 'tba_bodega_entrega_bien'
        verbose_name = 'Entrega de Bien/Activo'
        verbose_name_plural = 'Entregas de Bienes/Activos'
        ordering = ['-fecha_entrega']

    def __str__(self) -> str:
        """Representación en cadena de la entrega de bien."""
        return f"ENT-BIEN-{self.numero} - {self.fecha_entrega.strftime('%d/%m/%Y')}"


class DetalleEntregaBien(DetalleEntregaBase):
    """
    Detalle de bienes/activos entregados.
    Hereda de DetalleEntregaBase (DRY) y agrega campos específicos de bienes.
    """
    entrega = models.ForeignKey(
        EntregaBien,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Entrega'
    )
    activo = models.ForeignKey(
        'activos.Activo',
        on_delete=models.PROTECT,
        related_name='entregas_bienes',
        verbose_name='Activo/Bien'
    )
    numero_serie = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Número de Serie',
        help_text='Número de serie del bien entregado'
    )
    estado_fisico = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Estado Físico',
        help_text='Estado físico del bien al momento de la entrega'
    )

    class Meta:
        db_table = 'tba_bodega_entrega_bien_detalle'
        verbose_name = 'Detalle Entrega Bien'
        verbose_name_plural = 'Detalles Entrega Bienes'
        ordering = ['entrega', 'id']

    def __str__(self) -> str:
        """Representación en cadena del detalle de entrega de bien."""
        return f"{self.entrega.numero} - {self.activo} ({self.cantidad})"


