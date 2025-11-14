from django.contrib import admin
from .models import TipoReporte, ReporteGenerado, MovimientoInventario


@admin.register(TipoReporte)
class TipoReporteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'modulo', 'activo']
    list_filter = ['modulo', 'activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion']


@admin.register(ReporteGenerado)
class ReporteGeneradoAdmin(admin.ModelAdmin):
    list_display = ['tipo_reporte', 'usuario', 'fecha_generacion', 'formato', 'fecha_inicio', 'fecha_fin']
    list_filter = ['tipo_reporte', 'formato', 'fecha_generacion']
    search_fields = ['tipo_reporte__nombre', 'usuario__correo']
    readonly_fields = ['fecha_generacion']
    date_hierarchy = 'fecha_generacion'


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_movimiento', 'tipo_movimiento', 'activo',
        'bodega_origen', 'bodega_destino', 'cantidad',
        'stock_anterior', 'stock_nuevo', 'usuario'
    ]
    list_filter = ['tipo_movimiento', 'fecha_movimiento', 'bodega_origen', 'bodega_destino']
    search_fields = ['activo__codigo', 'activo__nombre', 'documento_referencia', 'usuario__correo']
    readonly_fields = ['fecha_movimiento']
    date_hierarchy = 'fecha_movimiento'
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('fecha_movimiento', 'tipo_movimiento', 'activo')
        }),
        ('Bodegas', {
            'fields': ('bodega_origen', 'bodega_destino')
        }),
        ('Cantidades', {
            'fields': ('cantidad', 'stock_anterior', 'stock_nuevo')
        }),
        ('Documento', {
            'fields': ('documento_referencia', 'tipo_documento')
        }),
        ('Responsable', {
            'fields': ('usuario', 'observaciones')
        }),
    )
