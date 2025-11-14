from django.contrib import admin

from .models import (
    Area,
    Departamento,
    DetalleSolicitud,
    Equipo,
    EstadoSolicitud,
    HistorialSolicitud,
    Solicitud,
    TipoSolicitud,
)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """Administración de departamentos."""

    list_display = ['codigo', 'nombre', 'responsable', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'eliminado', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion')
        }),
        ('Responsable', {
            'fields': ('responsable',)
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """Administración de áreas."""

    list_display = ['codigo', 'nombre', 'departamento', 'responsable', 'activo', 'fecha_creacion']
    list_filter = ['departamento', 'activo', 'eliminado', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['departamento']
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion', 'departamento')
        }),
        ('Responsable', {
            'fields': ('responsable',)
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    """Administración de equipos."""

    list_display = ['codigo', 'nombre', 'departamento', 'lider', 'activo', 'fecha_creacion']
    list_filter = ['departamento', 'activo', 'eliminado', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['departamento']
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion', 'departamento')
        }),
        ('Líder', {
            'fields': ('lider',)
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TipoSolicitud)
class TipoSolicitudAdmin(admin.ModelAdmin):
    """Administración de tipos de solicitud."""

    list_display = ['codigo', 'nombre', 'requiere_aprobacion', 'activo', 'fecha_creacion']
    list_filter = ['requiere_aprobacion', 'activo', 'eliminado', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('requiere_aprobacion',)
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EstadoSolicitud)
class EstadoSolicitudAdmin(admin.ModelAdmin):
    """Administración de estados de solicitud."""

    list_display = [
        'codigo', 'nombre', 'color', 'es_inicial', 'es_final',
        'requiere_accion', 'activo', 'fecha_creacion'
    ]
    list_filter = ['es_inicial', 'es_final', 'requiere_accion', 'activo', 'eliminado', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion', 'color')
        }),
        ('Configuración', {
            'fields': ('es_inicial', 'es_final', 'requiere_accion')
        }),
        ('Estado', {
            'fields': ('activo', 'eliminado')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class DetalleSolicitudInline(admin.TabularInline):
    """Inline para detalles de solicitud."""

    model = DetalleSolicitud
    extra = 1
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    fields = [
        'articulo', 'activo', 'cantidad_solicitada',
        'cantidad_aprobada', 'cantidad_despachada', 'observaciones'
    ]


class HistorialSolicitudInline(admin.TabularInline):
    """Inline para historial de solicitud."""

    model = HistorialSolicitud
    extra = 0
    readonly_fields = ['estado_anterior', 'estado_nuevo', 'usuario', 'fecha_cambio', 'observaciones']
    fields = ['estado_anterior', 'estado_nuevo', 'usuario', 'observaciones', 'fecha_cambio']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        """No permite agregar historial manualmente."""
        return False


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    """Administración de solicitudes."""

    list_display = [
        'numero', 'tipo', 'fecha_solicitud', 'tipo_solicitud',
        'estado', 'solicitante', 'departamento', 'area', 'activo'
    ]
    list_filter = [
        'tipo', 'tipo_solicitud', 'estado', 'fecha_solicitud',
        'fecha_requerida', 'departamento', 'area', 'bodega_origen',
        'activo', 'eliminado'
    ]
    search_fields = [
        'numero', 'solicitante__email', 'solicitante__username',
        'area_solicitante', 'titulo_actividad', 'motivo'
    ]
    readonly_fields = ['fecha_solicitud', 'fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['tipo_solicitud', 'estado', 'departamento', 'area', 'equipo']
    inlines = [DetalleSolicitudInline, HistorialSolicitudInline]
    date_hierarchy = 'fecha_solicitud'

    fieldsets = (
        ('Información General', {
            'fields': (
                'tipo', 'numero', 'fecha_solicitud', 'fecha_requerida',
                'tipo_solicitud', 'estado'
            )
        }),
        ('Información de la Actividad', {
            'fields': ('titulo_actividad', 'objetivo_actividad'),
            'classes': ('collapse',)
        }),
        ('Solicitante', {
            'fields': ('solicitante', 'area_solicitante', 'motivo')
        }),
        ('Estructura Organizacional', {
            'fields': ('departamento', 'area', 'equipo'),
            'classes': ('collapse',)
        }),
        ('Aprobación', {
            'fields': ('aprobador', 'fecha_aprobacion', 'notas_aprobacion'),
            'classes': ('collapse',)
        }),
        ('Despacho', {
            'fields': ('despachador', 'fecha_despacho', 'notas_despacho', 'bodega_origen'),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
        ('Estado y Auditoría', {
            'fields': ('activo', 'eliminado', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Campos de solo lectura según permisos."""
        readonly = list(self.readonly_fields)

        # Si la solicitud ya fue aprobada, no se puede editar ciertos campos
        if obj and obj.aprobador:
            readonly.extend(['tipo', 'tipo_solicitud', 'solicitante', 'departamento', 'area', 'equipo'])

        # Si ya fue despachada, es casi todo readonly
        if obj and obj.despachador:
            readonly.extend([
                'motivo', 'observaciones', 'titulo_actividad',
                'objetivo_actividad', 'area_solicitante', 'bodega_origen'
            ])

        return readonly


@admin.register(DetalleSolicitud)
class DetalleSolicitudAdmin(admin.ModelAdmin):
    """Administración de detalles de solicitud."""

    list_display = [
        'solicitud', 'get_producto', 'cantidad_solicitada',
        'cantidad_aprobada', 'cantidad_despachada', 'fecha_creacion'
    ]
    list_filter = ['solicitud__estado', 'solicitud__tipo', 'fecha_creacion', 'eliminado']
    search_fields = [
        'solicitud__numero', 'articulo__codigo', 'articulo__nombre',
        'activo__codigo', 'activo__nombre'
    ]
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['solicitud', 'articulo', 'activo']

    fieldsets = (
        ('Solicitud', {
            'fields': ('solicitud',)
        }),
        ('Producto', {
            'fields': ('articulo', 'activo'),
            'description': 'Debe especificar solo artículo o activo, no ambos.'
        }),
        ('Cantidades', {
            'fields': (
                'cantidad_solicitada', 'cantidad_aprobada', 'cantidad_despachada'
            )
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
        ('Estado y Auditoría', {
            'fields': ('eliminado', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_producto(self, obj):
        """Obtiene el nombre del producto (artículo o activo)."""
        return obj.producto_nombre if hasattr(obj, 'producto_nombre') else 'N/A'

    get_producto.short_description = 'Producto'


@admin.register(HistorialSolicitud)
class HistorialSolicitudAdmin(admin.ModelAdmin):
    """Administración de historial de solicitudes."""

    list_display = [
        'solicitud', 'estado_anterior', 'estado_nuevo',
        'usuario', 'fecha_cambio'
    ]
    list_filter = ['estado_nuevo', 'estado_anterior', 'fecha_cambio', 'eliminado']
    search_fields = [
        'solicitud__numero', 'usuario__email',
        'usuario__username', 'observaciones'
    ]
    readonly_fields = ['solicitud', 'estado_anterior', 'estado_nuevo', 'usuario', 'fecha_cambio', 'fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['solicitud']
    date_hierarchy = 'fecha_cambio'

    fieldsets = (
        ('Solicitud', {
            'fields': ('solicitud',)
        }),
        ('Cambio de Estado', {
            'fields': ('estado_anterior', 'estado_nuevo', 'usuario', 'fecha_cambio')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('eliminado', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """No permite crear historial manualmente."""
        return False

    def has_delete_permission(self, request, obj=None):
        """No permite eliminar historial."""
        return False
