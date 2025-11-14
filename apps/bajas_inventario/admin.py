"""
Configuración del admin de Django para el módulo de bajas de inventario.

Registra todos los modelos del módulo con sus respectivas
configuraciones de visualización, filtros y búsqueda.
"""
from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import MotivoBaja, BajaInventario


@admin.register(MotivoBaja)
class MotivoBajaAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo MotivoBaja."""

    list_display = ['codigo', 'nombre', 'activo', 'eliminado', 'fecha_creacion']
    list_filter = ['activo', 'eliminado']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    ordering = ['codigo']

    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion')
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BajaInventario)
class BajaInventarioAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo BajaInventario."""

    list_display = [
        'numero', 'fecha_baja', 'get_activo_info', 'motivo',
        'ubicacion', 'solicitante', 'eliminado', 'fecha_creacion'
    ]
    list_filter = [
        'motivo', 'fecha_baja', 'ubicacion', 'eliminado'
    ]
    search_fields = [
        'numero', 'activo__codigo', 'activo__nombre',
        'solicitante__username', 'observaciones'
    ]
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    ordering = ['-fecha_baja', '-numero']
    list_per_page = 25

    fieldsets = (
        ('Información General', {
            'fields': ('numero', 'fecha_baja', 'activo', 'motivo', 'ubicacion')
        }),
        ('Responsable', {
            'fields': ('solicitante',)
        }),
        ('Detalles', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('eliminado', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_activo_info(self, obj: BajaInventario) -> str:
        """Muestra el código y nombre del activo dado de baja."""
        if obj.activo:
            return f"{obj.activo.codigo} - {obj.activo.nombre}"
        return "-"
    get_activo_info.short_description = 'Activo'

    def get_queryset(self, request: HttpRequest) -> QuerySet[BajaInventario]:
        """Optimiza consultas con select_related."""
        qs = super().get_queryset(request)
        return qs.select_related(
            'activo', 'motivo', 'ubicacion', 'solicitante',
            'activo__categoria', 'activo__estado'
        )
