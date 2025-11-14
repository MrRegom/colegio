from django.contrib import admin
from .models import (
    Bodega, UnidadMedida, Categoria, Articulo, TipoMovimiento, Movimiento,
    EstadoEntrega, TipoEntrega, EntregaArticulo, DetalleEntregaArticulo,
    EntregaBien, DetalleEntregaBien
)


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'responsable', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    """
    Administración de Unidades de Medida en el panel de Django Admin.

    Este modelo pertenece al módulo de BODEGA, no al módulo de activos.
    """
    list_display = ['codigo', 'nombre', 'simbolo', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'simbolo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    ordering = ['codigo']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    """
    Administración de Artículos en el panel de Django Admin.
    """
    list_display = ['codigo', 'nombre', 'categoria', 'stock_actual', 'stock_minimo', 'ubicacion_fisica', 'activo']
    list_filter = ['categoria', 'ubicacion_fisica', 'activo', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'descripcion', 'codigo_barras']
    readonly_fields = ['stock_actual', 'codigo_barras', 'fecha_creacion', 'fecha_actualizacion']
    filter_horizontal = ['marcas', 'unidades_medida']

    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion', 'codigo_barras', 'categoria')
        }),
        ('Marcas y Unidades', {
            'fields': ('marcas', 'unidades_medida')
        }),
        ('Stock', {
            'fields': ('stock_actual', 'stock_minimo', 'stock_maximo', 'punto_reorden')
        }),
        ('Ubicación', {
            'fields': ('ubicacion_fisica',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )


@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['articulo', 'tipo', 'operacion', 'cantidad', 'usuario', 'stock_antes', 'stock_despues', 'fecha_creacion']
    list_filter = ['operacion', 'tipo', 'fecha_creacion']
    search_fields = ['articulo__codigo', 'articulo__nombre', 'usuario__correo', 'motivo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_creacion'


# ==================== ENTREGA ADMIN ====================

@admin.register(EstadoEntrega)
class EstadoEntregaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'color', 'es_inicial', 'es_final', 'activo']
    list_filter = ['activo', 'es_inicial', 'es_final']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(TipoEntrega)
class TipoEntregaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'requiere_autorizacion', 'activo']
    list_filter = ['activo', 'requiere_autorizacion']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


class DetalleEntregaArticuloInline(admin.TabularInline):
    model = DetalleEntregaArticulo
    extra = 1
    readonly_fields = ['fecha_creacion']
    fields = ['articulo', 'cantidad', 'lote', 'observaciones']


@admin.register(EntregaArticulo)
class EntregaArticuloAdmin(admin.ModelAdmin):
    list_display = ['numero', 'fecha_entrega', 'bodega_origen', 'tipo', 'estado', 'recibido_por', 'entregado_por']
    list_filter = ['estado', 'tipo', 'bodega_origen', 'fecha_entrega']
    search_fields = ['numero', 'recibido_por', 'rut_receptor', 'documento_referencia']
    readonly_fields = ['numero', 'fecha_entrega', 'fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_entrega'
    inlines = [DetalleEntregaArticuloInline]

    fieldsets = (
        ('Información General', {
            'fields': ('numero', 'fecha_entrega', 'bodega_origen', 'tipo', 'estado')
        }),
        ('Receptor', {
            'fields': ('recibido_por', 'rut_receptor', 'departamento_destino')
        }),
        ('Documentación', {
            'fields': ('documento_referencia', 'motivo', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('entregado_por', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )


class DetalleEntregaBienInline(admin.TabularInline):
    model = DetalleEntregaBien
    extra = 1
    readonly_fields = ['fecha_creacion']
    fields = ['equipo', 'cantidad', 'numero_serie', 'estado_fisico', 'observaciones']


@admin.register(EntregaBien)
class EntregaBienAdmin(admin.ModelAdmin):
    list_display = ['numero', 'fecha_entrega', 'tipo', 'estado', 'recibido_por', 'entregado_por']
    list_filter = ['estado', 'tipo', 'fecha_entrega']
    search_fields = ['numero', 'recibido_por', 'rut_receptor', 'documento_referencia']
    readonly_fields = ['numero', 'fecha_entrega', 'fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_entrega'
    inlines = [DetalleEntregaBienInline]

    fieldsets = (
        ('Información General', {
            'fields': ('numero', 'fecha_entrega', 'tipo', 'estado')
        }),
        ('Receptor', {
            'fields': ('recibido_por', 'rut_receptor', 'departamento_destino')
        }),
        ('Documentación', {
            'fields': ('documento_referencia', 'motivo', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('entregado_por', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )
