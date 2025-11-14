from django.contrib import admin
from .models import (
    Proveedor, EstadoOrdenCompra, OrdenCompra, DetalleOrdenCompra, DetalleOrdenCompraArticulo,
    EstadoRecepcion, TipoRecepcion, RecepcionArticulo, DetalleRecepcionArticulo,
    RecepcionActivo, DetalleRecepcionActivo
)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    """Administrador del modelo Proveedor."""

    list_display = ['rut', 'razon_social', 'telefono', 'email', 'ciudad', 'activo']
    list_filter = ['activo', 'ciudad']
    search_fields = ['rut', 'razon_social', 'email']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('rut', 'razon_social')
        }),
        ('Contacto', {
            'fields': ('direccion', 'comuna', 'ciudad', 'telefono', 'email', 'sitio_web')
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EstadoOrdenCompra)
class EstadoOrdenCompraAdmin(admin.ModelAdmin):
    """Administrador del catálogo de estados de órdenes de compra."""

    list_display = ['codigo', 'nombre', 'color', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información', {
            'fields': ('codigo', 'nombre', 'descripcion', 'color')
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EstadoRecepcion)
class EstadoRecepcionAdmin(admin.ModelAdmin):
    """Administrador del catálogo de estados de recepción."""

    list_display = ['codigo', 'nombre', 'color', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información', {
            'fields': ('codigo', 'nombre', 'descripcion', 'color')
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TipoRecepcion)
class TipoRecepcionAdmin(admin.ModelAdmin):
    """Administrador del catálogo de tipos de recepción."""

    list_display = ['codigo', 'nombre', 'requiere_orden', 'activo']
    list_filter = ['requiere_orden', 'activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información', {
            'fields': ('codigo', 'nombre', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('requiere_orden',)
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class DetalleOrdenCompraInline(admin.TabularInline):
    """Inline para detalles de activos en orden de compra."""

    model = DetalleOrdenCompra
    extra = 1
    readonly_fields = ['subtotal']
    fields = ['activo', 'cantidad', 'precio_unitario', 'descuento', 'subtotal', 'cantidad_recibida']


class DetalleOrdenCompraArticuloInline(admin.TabularInline):
    """Inline para detalles de artículos en orden de compra."""

    model = DetalleOrdenCompraArticulo
    extra = 1
    readonly_fields = ['subtotal']
    fields = ['articulo', 'cantidad', 'precio_unitario', 'descuento', 'subtotal', 'cantidad_recibida']


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    """Administrador del modelo Orden de Compra."""

    list_display = ['numero', 'fecha_orden', 'proveedor', 'estado', 'total', 'solicitante']
    list_filter = ['estado', 'fecha_orden', 'bodega_destino']
    search_fields = ['numero', 'proveedor__razon_social']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'subtotal', 'impuesto', 'total']
    inlines = [DetalleOrdenCompraArticuloInline, DetalleOrdenCompraInline]
    fieldsets = (
        ('Información General', {
            'fields': ('numero', 'fecha_orden', 'fecha_entrega_esperada', 'fecha_entrega_real')
        }),
        ('Proveedor y Destino', {
            'fields': ('proveedor', 'bodega_destino')
        }),
        ('Estado y Responsables', {
            'fields': ('estado', 'solicitante', 'aprobador')
        }),
        ('Montos', {
            'fields': ('subtotal', 'impuesto', 'descuento', 'total')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class DetalleRecepcionArticuloInline(admin.TabularInline):
    """Inline para detalles de artículos en recepción."""

    model = DetalleRecepcionArticulo
    extra = 1
    fields = ['articulo', 'cantidad', 'lote', 'fecha_vencimiento', 'observaciones']


@admin.register(RecepcionArticulo)
class RecepcionArticuloAdmin(admin.ModelAdmin):
    """Administrador del modelo Recepción de Artículos."""

    list_display = ['numero', 'fecha_recepcion', 'orden_compra', 'bodega', 'estado', 'recibido_por']
    list_filter = ['estado', 'bodega', 'fecha_recepcion']
    search_fields = ['numero', 'documento_referencia']
    readonly_fields = ['fecha_recepcion', 'fecha_creacion', 'fecha_actualizacion']
    inlines = [DetalleRecepcionArticuloInline]
    fieldsets = (
        ('Información General', {
            'fields': ('numero', 'fecha_recepcion', 'tipo', 'orden_compra')
        }),
        ('Destino', {
            'fields': ('bodega',)
        }),
        ('Estado y Responsable', {
            'fields': ('estado', 'recibido_por')
        }),
        ('Documentación', {
            'fields': ('documento_referencia', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class DetalleRecepcionActivoInline(admin.TabularInline):
    """Inline para detalles de activos en recepción."""

    model = DetalleRecepcionActivo
    extra = 1
    fields = ['activo', 'cantidad', 'numero_serie', 'observaciones']


@admin.register(RecepcionActivo)
class RecepcionActivoAdmin(admin.ModelAdmin):
    """Administrador del modelo Recepción de Activos."""

    list_display = ['numero', 'fecha_recepcion', 'orden_compra', 'estado', 'recibido_por']
    list_filter = ['estado', 'fecha_recepcion']
    search_fields = ['numero', 'documento_referencia']
    readonly_fields = ['fecha_recepcion', 'fecha_creacion', 'fecha_actualizacion']
    inlines = [DetalleRecepcionActivoInline]
    fieldsets = (
        ('Información General', {
            'fields': ('numero', 'fecha_recepcion', 'tipo', 'orden_compra')
        }),
        ('Estado y Responsable', {
            'fields': ('estado', 'recibido_por')
        }),
        ('Documentación', {
            'fields': ('documento_referencia', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
