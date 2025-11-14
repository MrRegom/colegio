"""
Repository Pattern para el módulo de solicitudes.

Separa la lógica de acceso a datos de la lógica de negocio,
siguiendo el principio de Inversión de Dependencias (SOLID).
"""
from typing import Optional
from django.db.models import QuerySet
from django.contrib.auth.models import User
from .models import (
    Departamento, Area, Equipo,
    TipoSolicitud, EstadoSolicitud, Solicitud,
    DetalleSolicitud, HistorialSolicitud
)
from apps.bodega.models import Bodega


# ==================== DEPARTAMENTO REPOSITORY ====================

class DepartamentoRepository:
    """Repository para gestionar acceso a datos de Departamentos."""

    @staticmethod
    def get_all() -> QuerySet[Departamento]:
        """Retorna todos los departamentos activos y no eliminados."""
        return Departamento.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(departamento_id: int) -> Optional[Departamento]:
        """Obtiene un departamento por su ID."""
        try:
            return Departamento.objects.get(id=departamento_id, eliminado=False, activo=True)
        except Departamento.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Departamento]:
        """Obtiene un departamento por su código."""
        try:
            return Departamento.objects.get(codigo=codigo, eliminado=False, activo=True)
        except Departamento.DoesNotExist:
            return None


# ==================== AREA REPOSITORY ====================

class AreaRepository:
    """Repository para gestionar áreas."""

    @staticmethod
    def get_all() -> QuerySet[Area]:
        """Retorna todas las áreas activas y no eliminadas."""
        return Area.objects.filter(
            activo=True, eliminado=False
        ).select_related('departamento').order_by('codigo')

    @staticmethod
    def get_by_id(area_id: int) -> Optional[Area]:
        """Obtiene un área por su ID."""
        try:
            return Area.objects.select_related('departamento').get(
                id=area_id, eliminado=False, activo=True
            )
        except Area.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Area]:
        """Obtiene un área por su código."""
        try:
            return Area.objects.select_related('departamento').get(
                codigo=codigo, eliminado=False, activo=True
            )
        except Area.DoesNotExist:
            return None

    @staticmethod
    def filter_by_departamento(departamento: Departamento) -> QuerySet[Area]:
        """Retorna áreas de un departamento específico."""
        return Area.objects.filter(
            departamento=departamento,
            activo=True,
            eliminado=False
        ).order_by('codigo')


# ==================== EQUIPO REPOSITORY ====================

class EquipoRepository:
    """Repository para gestionar equipos."""

    @staticmethod
    def get_all() -> QuerySet[Equipo]:
        """Retorna todos los equipos activos y no eliminados."""
        return Equipo.objects.filter(
            activo=True, eliminado=False
        ).select_related('departamento').order_by('codigo')

    @staticmethod
    def get_by_id(equipo_id: int) -> Optional[Equipo]:
        """Obtiene un equipo por su ID."""
        try:
            return Equipo.objects.select_related('departamento').get(
                id=equipo_id, eliminado=False, activo=True
            )
        except Equipo.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Equipo]:
        """Obtiene un equipo por su código."""
        try:
            return Equipo.objects.select_related('departamento').get(
                codigo=codigo, eliminado=False, activo=True
            )
        except Equipo.DoesNotExist:
            return None

    @staticmethod
    def filter_by_departamento(departamento: Departamento) -> QuerySet[Equipo]:
        """Retorna equipos de un departamento específico."""
        return Equipo.objects.filter(
            departamento=departamento,
            activo=True,
            eliminado=False
        ).order_by('codigo')


# ==================== TIPO SOLICITUD REPOSITORY ====================

class TipoSolicitudRepository:
    """Repository para gestionar acceso a datos de Tipos de Solicitud."""

    @staticmethod
    def get_all() -> QuerySet[TipoSolicitud]:
        """Retorna todos los tipos activos y no eliminados."""
        return TipoSolicitud.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(tipo_id: int) -> Optional[TipoSolicitud]:
        """Obtiene un tipo por su ID."""
        try:
            return TipoSolicitud.objects.get(id=tipo_id, eliminado=False, activo=True)
        except TipoSolicitud.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[TipoSolicitud]:
        """Obtiene un tipo por su código."""
        try:
            return TipoSolicitud.objects.get(codigo=codigo, eliminado=False, activo=True)
        except TipoSolicitud.DoesNotExist:
            return None

    @staticmethod
    def get_with_aprobacion() -> QuerySet[TipoSolicitud]:
        """Retorna tipos que requieren aprobación."""
        return TipoSolicitud.objects.filter(
            requiere_aprobacion=True, activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_without_aprobacion() -> QuerySet[TipoSolicitud]:
        """Retorna tipos que NO requieren aprobación."""
        return TipoSolicitud.objects.filter(
            requiere_aprobacion=False, activo=True, eliminado=False
        ).order_by('codigo')


# ==================== ESTADO SOLICITUD REPOSITORY ====================

class EstadoSolicitudRepository:
    """Repository para gestionar estados de solicitudes."""

    @staticmethod
    def get_all() -> QuerySet[EstadoSolicitud]:
        """Retorna todos los estados activos y no eliminados."""
        return EstadoSolicitud.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(estado_id: int) -> Optional[EstadoSolicitud]:
        """Obtiene un estado por su ID."""
        try:
            return EstadoSolicitud.objects.get(id=estado_id, eliminado=False, activo=True)
        except EstadoSolicitud.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[EstadoSolicitud]:
        """Obtiene un estado por su código."""
        try:
            return EstadoSolicitud.objects.get(codigo=codigo, eliminado=False, activo=True)
        except EstadoSolicitud.DoesNotExist:
            return None

    @staticmethod
    def get_inicial() -> Optional[EstadoSolicitud]:
        """Obtiene el estado inicial del sistema."""
        return EstadoSolicitud.objects.filter(
            es_inicial=True, activo=True, eliminado=False
        ).first()

    @staticmethod
    def get_finales() -> QuerySet[EstadoSolicitud]:
        """Retorna todos los estados finales."""
        return EstadoSolicitud.objects.filter(
            es_final=True, activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_que_requieren_accion() -> QuerySet[EstadoSolicitud]:
        """Retorna estados que requieren acción."""
        return EstadoSolicitud.objects.filter(
            requiere_accion=True, activo=True, eliminado=False
        ).order_by('codigo')


# ==================== SOLICITUD REPOSITORY ====================

class SolicitudRepository:
    """Repository para gestionar solicitudes."""

    @staticmethod
    def get_all() -> QuerySet[Solicitud]:
        """Retorna todas las solicitudes no eliminadas con relaciones optimizadas."""
        return Solicitud.objects.filter(
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'estado', 'solicitante',
            'aprobador', 'despachador', 'bodega_origen'
        ).order_by('-fecha_solicitud', '-numero')

    @staticmethod
    def get_by_id(solicitud_id: int) -> Optional[Solicitud]:
        """Obtiene una solicitud por su ID."""
        try:
            return Solicitud.objects.select_related(
                'tipo_solicitud', 'estado', 'solicitante',
                'aprobador', 'despachador', 'bodega_origen'
            ).get(id=solicitud_id, eliminado=False)
        except Solicitud.DoesNotExist:
            return None

    @staticmethod
    def get_by_numero(numero: str) -> Optional[Solicitud]:
        """Obtiene una solicitud por su número."""
        try:
            return Solicitud.objects.select_related(
                'tipo_solicitud', 'estado', 'solicitante',
                'aprobador', 'despachador', 'bodega_origen'
            ).get(numero=numero, eliminado=False)
        except Solicitud.DoesNotExist:
            return None

    @staticmethod
    def filter_by_solicitante(solicitante: User) -> QuerySet[Solicitud]:
        """Retorna solicitudes de un solicitante específico."""
        return Solicitud.objects.filter(
            solicitante=solicitante,
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'estado', 'aprobador', 'despachador', 'bodega_origen'
        ).order_by('-fecha_solicitud')

    @staticmethod
    def filter_by_estado(estado: EstadoSolicitud) -> QuerySet[Solicitud]:
        """Retorna solicitudes en un estado específico."""
        return Solicitud.objects.filter(
            estado=estado,
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'solicitante', 'aprobador', 'despachador', 'bodega_origen'
        ).order_by('-fecha_solicitud')

    @staticmethod
    def filter_by_tipo(tipo_solicitud: TipoSolicitud) -> QuerySet[Solicitud]:
        """Retorna solicitudes de un tipo específico."""
        return Solicitud.objects.filter(
            tipo_solicitud=tipo_solicitud,
            eliminado=False
        ).select_related(
            'estado', 'solicitante', 'aprobador', 'despachador', 'bodega_origen'
        ).order_by('-fecha_solicitud')

    @staticmethod
    def filter_by_tipo_choice(tipo: str) -> QuerySet[Solicitud]:
        """Retorna solicitudes por tipo de choice (ACTIVO o ARTICULO)."""
        return Solicitud.objects.filter(
            tipo=tipo,
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'estado', 'solicitante',
            'aprobador', 'despachador', 'bodega_origen'
        ).order_by('-fecha_solicitud')

    @staticmethod
    def filter_by_bodega(bodega: Bodega) -> QuerySet[Solicitud]:
        """Retorna solicitudes de una bodega específica."""
        return Solicitud.objects.filter(
            bodega_origen=bodega,
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'estado', 'solicitante',
            'aprobador', 'despachador'
        ).order_by('-fecha_solicitud')

    @staticmethod
    def filter_pendientes_aprobacion() -> QuerySet[Solicitud]:
        """Retorna solicitudes pendientes de aprobación."""
        return Solicitud.objects.filter(
            estado__requiere_accion=True,
            aprobador__isnull=True,
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'estado', 'solicitante', 'bodega_origen'
        ).order_by('-fecha_solicitud')

    @staticmethod
    def filter_pendientes_despacho() -> QuerySet[Solicitud]:
        """Retorna solicitudes pendientes de despacho."""
        return Solicitud.objects.filter(
            aprobador__isnull=False,
            despachador__isnull=True,
            estado__es_final=False,
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'estado', 'solicitante',
            'aprobador', 'bodega_origen'
        ).order_by('-fecha_solicitud')

    @staticmethod
    def exists_by_numero(numero: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe una solicitud con el número dado."""
        queryset = Solicitud.objects.filter(numero=numero)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    @staticmethod
    def search(query: str) -> QuerySet[Solicitud]:
        """Búsqueda de solicitudes por número o solicitante."""
        from django.db.models import Q
        return Solicitud.objects.filter(
            Q(numero__icontains=query) |
            Q(solicitante__first_name__icontains=query) |
            Q(solicitante__last_name__icontains=query) |
            Q(solicitante__email__icontains=query) |
            Q(area_solicitante__icontains=query),
            eliminado=False
        ).select_related(
            'tipo_solicitud', 'estado', 'solicitante',
            'aprobador', 'despachador', 'bodega_origen'
        ).order_by('-fecha_solicitud')


# ==================== DETALLE SOLICITUD REPOSITORY ====================

class DetalleSolicitudRepository:
    """Repository para detalles de solicitudes."""

    @staticmethod
    def filter_by_solicitud(solicitud: Solicitud) -> QuerySet[DetalleSolicitud]:
        """Retorna detalles de una solicitud específica."""
        return DetalleSolicitud.objects.filter(
            solicitud=solicitud,
            eliminado=False
        ).select_related('activo').order_by('id')

    @staticmethod
    def get_by_id(detalle_id: int) -> Optional[DetalleSolicitud]:
        """Obtiene un detalle por su ID."""
        try:
            return DetalleSolicitud.objects.select_related(
                'solicitud', 'activo'
            ).get(id=detalle_id, eliminado=False)
        except DetalleSolicitud.DoesNotExist:
            return None

    @staticmethod
    def filter_pendientes_despacho(solicitud: Solicitud) -> QuerySet[DetalleSolicitud]:
        """Retorna detalles pendientes de despacho."""
        from django.db.models import F
        return DetalleSolicitud.objects.filter(
            solicitud=solicitud,
            cantidad_aprobada__gt=F('cantidad_despachada'),
            eliminado=False
        ).select_related('activo').order_by('id')


# ==================== HISTORIAL SOLICITUD REPOSITORY ====================

class HistorialSolicitudRepository:
    """Repository para historial de cambios de estado."""

    @staticmethod
    def filter_by_solicitud(solicitud: Solicitud) -> QuerySet[HistorialSolicitud]:
        """Retorna el historial de una solicitud específica."""
        return HistorialSolicitud.objects.filter(
            solicitud=solicitud,
            eliminado=False
        ).select_related(
            'estado_anterior', 'estado_nuevo', 'usuario'
        ).order_by('-fecha_cambio')

    @staticmethod
    def get_by_id(historial_id: int) -> Optional[HistorialSolicitud]:
        """Obtiene un registro de historial por su ID."""
        try:
            return HistorialSolicitud.objects.select_related(
                'solicitud', 'estado_anterior', 'estado_nuevo', 'usuario'
            ).get(id=historial_id, eliminado=False)
        except HistorialSolicitud.DoesNotExist:
            return None

    @staticmethod
    def create(
        solicitud: Solicitud,
        estado_anterior: Optional[EstadoSolicitud],
        estado_nuevo: EstadoSolicitud,
        usuario: User,
        observaciones: str = ''
    ) -> HistorialSolicitud:
        """Crea un nuevo registro de historial."""
        return HistorialSolicitud.objects.create(
            solicitud=solicitud,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            usuario=usuario,
            observaciones=observaciones
        )
