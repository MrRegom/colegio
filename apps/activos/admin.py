"""
Configuración del admin de Django para el módulo de activos.

Registra todos los modelos del módulo con sus respectivas
configuraciones de visualización, filtros y búsqueda.
"""
from __future__ import annotations

from typing import Any

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import (
    CategoriaActivo, EstadoActivo, Activo, Ubicacion,
    Proveniencia, Marca, Taller, TipoMovimientoActivo, MovimientoActivo
)


@admin.register(CategoriaActivo)
class CategoriaActivoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo', 'eliminado', 'fecha_creacion']
    list_filter = ['activo', 'eliminado']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(EstadoActivo)
class EstadoActivoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'color', 'es_inicial', 'permite_movimiento', 'activo', 'eliminado']
    list_filter = ['es_inicial', 'permite_movimiento', 'activo', 'eliminado']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Activo."""

    list_display = ['codigo', 'nombre', 'categoria', 'marca', 'estado', 'precio_unitario', 'activo', 'eliminado']
    list_filter = ['categoria', 'estado', 'marca', 'activo', 'eliminado', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'numero_serie', 'codigo_barras']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'codigo_barras']
    list_per_page = 25

    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion', 'categoria', 'estado')
        }),
        ('Detalles del Activo', {
            'fields': ('marca', 'lote', 'numero_serie', 'codigo_barras')
        }),
        ('Precio', {
            'fields': ('precio_unitario',)
        }),
        ('Estado del Registro', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Activo]:
        """Optimiza consultas con select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('categoria', 'estado', 'marca')


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Ubicacion."""

    list_display = ['codigo', 'nombre', 'activo', 'eliminado', 'fecha_creacion']
    list_filter = ['activo', 'eliminado']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Proveniencia)
class ProvenienciaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo', 'eliminado', 'fecha_creacion']
    list_filter = ['activo', 'eliminado']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(TipoMovimientoActivo)
class TipoMovimientoActivoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo TipoMovimientoActivo."""

    list_display = ['codigo', 'nombre', 'activo', 'eliminado', 'fecha_creacion']
    list_filter = ['activo', 'eliminado']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(MovimientoActivo)
class MovimientoActivoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo MovimientoActivo."""

    list_display = [
        'activo', 'tipo_movimiento', 'ubicacion_destino', 'taller',
        'responsable', 'proveniencia', 'fecha_creacion', 'usuario_registro'
    ]
    list_filter = ['tipo_movimiento', 'ubicacion_destino', 'taller', 'proveniencia', 'fecha_creacion']
    search_fields = ['activo__codigo', 'activo__nombre', 'responsable__username']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'usuario_registro']
    list_per_page = 25

    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('activo', 'tipo_movimiento', 'usuario_registro')
        }),
        ('Destino', {
            'fields': ('ubicacion_destino', 'taller', 'responsable')
        }),
        ('Procedencia', {
            'fields': ('proveniencia',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[MovimientoActivo]:
        """Optimiza consultas con select_related."""
        qs = super().get_queryset(request)
        return qs.select_related(
            'activo', 'tipo_movimiento', 'ubicacion_destino',
            'taller', 'responsable', 'proveniencia', 'usuario_registro'
        )

    def save_model(self, request: HttpRequest, obj: MovimientoActivo,
                   form: Any, change: bool) -> None:
        """Asigna el usuario actual si es un nuevo registro."""
        if not change:  # Solo al crear
            obj.usuario_registro = request.user
        super().save_model(request, obj, form, change)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Marca."""

    list_display = ['codigo', 'nombre', 'activo', 'eliminado', 'fecha_creacion']
    list_filter = ['activo', 'eliminado']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

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


@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Taller."""

    list_display = ['codigo', 'nombre', 'ubicacion', 'responsable', 'activo', 'eliminado']
    list_filter = ['activo', 'eliminado', 'responsable']
    search_fields = ['codigo', 'nombre', 'ubicacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion', 'ubicacion')
        }),
        ('Gestión', {
            'fields': ('responsable', 'observaciones')
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Taller]:
        """Optimiza consultas con select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('responsable')
