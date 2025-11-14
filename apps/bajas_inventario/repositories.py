"""
Repository Pattern para el módulo de bajas de inventario.

Separa la lógica de acceso a datos de la lógica de negocio,
siguiendo el principio de Inversión de Dependencias (SOLID).
"""
from typing import Optional
from django.db.models import QuerySet
from django.contrib.auth.models import User
from .models import (
    MotivoBaja, EstadoBaja, BajaInventario,
    DetalleBaja, HistorialBaja
)
from apps.bodega.models import Bodega


# ==================== MOTIVO BAJA REPOSITORY ====================

class MotivoBajaRepository:
    """Repository para gestionar acceso a datos de Motivos de Baja."""

    @staticmethod
    def get_all() -> QuerySet[MotivoBaja]:
        """Retorna todos los motivos activos y no eliminados."""
        return MotivoBaja.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(motivo_id: int) -> Optional[MotivoBaja]:
        """Obtiene un motivo por su ID."""
        try:
            return MotivoBaja.objects.get(id=motivo_id, eliminado=False, activo=True)
        except MotivoBaja.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[MotivoBaja]:
        """Obtiene un motivo por su código."""
        try:
            return MotivoBaja.objects.get(codigo=codigo, eliminado=False, activo=True)
        except MotivoBaja.DoesNotExist:
            return None

    @staticmethod
    def get_with_autorizacion() -> QuerySet[MotivoBaja]:
        """Retorna motivos que requieren autorización."""
        return MotivoBaja.objects.filter(
            requiere_autorizacion=True, activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_with_documento() -> QuerySet[MotivoBaja]:
        """Retorna motivos que requieren documento."""
        return MotivoBaja.objects.filter(
            requiere_documento=True, activo=True, eliminado=False
        ).order_by('codigo')


# ==================== ESTADO BAJA REPOSITORY ====================

class EstadoBajaRepository:
    """Repository para gestionar estados de bajas de inventario."""

    @staticmethod
    def get_all() -> QuerySet[EstadoBaja]:
        """Retorna todos los estados activos y no eliminados."""
        return EstadoBaja.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(estado_id: int) -> Optional[EstadoBaja]:
        """Obtiene un estado por su ID."""
        try:
            return EstadoBaja.objects.get(id=estado_id, eliminado=False, activo=True)
        except EstadoBaja.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[EstadoBaja]:
        """Obtiene un estado por su código."""
        try:
            return EstadoBaja.objects.get(codigo=codigo, eliminado=False, activo=True)
        except EstadoBaja.DoesNotExist:
            return None

    @staticmethod
    def get_inicial() -> Optional[EstadoBaja]:
        """Obtiene el estado inicial del sistema."""
        return EstadoBaja.objects.filter(
            es_inicial=True, activo=True, eliminado=False
        ).first()

    @staticmethod
    def get_finales() -> QuerySet[EstadoBaja]:
        """Retorna todos los estados finales."""
        return EstadoBaja.objects.filter(
            es_final=True, activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_que_permiten_edicion() -> QuerySet[EstadoBaja]:
        """Retorna estados que permiten edición."""
        return EstadoBaja.objects.filter(
            permite_edicion=True, activo=True, eliminado=False
        ).order_by('codigo')


# ==================== BAJA INVENTARIO REPOSITORY ====================

class BajaInventarioRepository:
    """Repository para gestionar bajas de inventario."""

    @staticmethod
    def get_all() -> QuerySet[BajaInventario]:
        """Retorna todas las bajas no eliminadas con relaciones optimizadas."""
        return BajaInventario.objects.filter(
            eliminado=False
        ).select_related(
            'motivo', 'estado', 'bodega', 'solicitante', 'autorizador'
        ).order_by('-fecha_baja', '-numero')

    @staticmethod
    def get_by_id(baja_id: int) -> Optional[BajaInventario]:
        """Obtiene una baja por su ID."""
        try:
            return BajaInventario.objects.select_related(
                'motivo', 'estado', 'bodega', 'solicitante', 'autorizador'
            ).get(id=baja_id, eliminado=False)
        except BajaInventario.DoesNotExist:
            return None

    @staticmethod
    def get_by_numero(numero: str) -> Optional[BajaInventario]:
        """Obtiene una baja por su número."""
        try:
            return BajaInventario.objects.select_related(
                'motivo', 'estado', 'bodega', 'solicitante', 'autorizador'
            ).get(numero=numero, eliminado=False)
        except BajaInventario.DoesNotExist:
            return None

    @staticmethod
    def filter_by_solicitante(solicitante: User) -> QuerySet[BajaInventario]:
        """Retorna bajas de un solicitante específico."""
        return BajaInventario.objects.filter(
            solicitante=solicitante,
            eliminado=False
        ).select_related(
            'motivo', 'estado', 'bodega', 'autorizador'
        ).order_by('-fecha_baja')

    @staticmethod
    def filter_by_estado(estado: EstadoBaja) -> QuerySet[BajaInventario]:
        """Retorna bajas en un estado específico."""
        return BajaInventario.objects.filter(
            estado=estado,
            eliminado=False
        ).select_related(
            'motivo', 'bodega', 'solicitante', 'autorizador'
        ).order_by('-fecha_baja')

    @staticmethod
    def filter_by_motivo(motivo: MotivoBaja) -> QuerySet[BajaInventario]:
        """Retorna bajas de un motivo específico."""
        return BajaInventario.objects.filter(
            motivo=motivo,
            eliminado=False
        ).select_related(
            'estado', 'bodega', 'solicitante', 'autorizador'
        ).order_by('-fecha_baja')

    @staticmethod
    def filter_by_bodega(bodega: Bodega) -> QuerySet[BajaInventario]:
        """Retorna bajas de una bodega específica."""
        return BajaInventario.objects.filter(
            bodega=bodega,
            eliminado=False
        ).select_related(
            'motivo', 'estado', 'solicitante', 'autorizador'
        ).order_by('-fecha_baja')

    @staticmethod
    def filter_pendientes_autorizacion() -> QuerySet[BajaInventario]:
        """Retorna bajas pendientes de autorización."""
        return BajaInventario.objects.filter(
            autorizador__isnull=True,
            eliminado=False
        ).select_related(
            'motivo', 'estado', 'bodega', 'solicitante'
        ).order_by('-fecha_baja')

    @staticmethod
    def exists_by_numero(numero: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe una baja con el número dado."""
        queryset = BajaInventario.objects.filter(numero=numero)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    @staticmethod
    def search(query: str) -> QuerySet[BajaInventario]:
        """Búsqueda de bajas por número o solicitante."""
        from django.db.models import Q
        return BajaInventario.objects.filter(
            Q(numero__icontains=query) |
            Q(solicitante__first_name__icontains=query) |
            Q(solicitante__last_name__icontains=query) |
            Q(descripcion__icontains=query),
            eliminado=False
        ).select_related(
            'motivo', 'estado', 'bodega', 'solicitante', 'autorizador'
        ).order_by('-fecha_baja')


# ==================== DETALLE BAJA REPOSITORY ====================

class DetalleBajaRepository:
    """Repository para detalles de bajas de inventario."""

    @staticmethod
    def filter_by_baja(baja: BajaInventario) -> QuerySet[DetalleBaja]:
        """Retorna detalles de una baja específica."""
        return DetalleBaja.objects.filter(
            baja=baja,
            eliminado=False
        ).select_related('activo').order_by('id')

    @staticmethod
    def get_by_id(detalle_id: int) -> Optional[DetalleBaja]:
        """Obtiene un detalle por su ID."""
        try:
            return DetalleBaja.objects.select_related(
                'baja', 'activo'
            ).get(id=detalle_id, eliminado=False)
        except DetalleBaja.DoesNotExist:
            return None


# ==================== HISTORIAL BAJA REPOSITORY ====================

class HistorialBajaRepository:
    """Repository para historial de cambios de estado de bajas."""

    @staticmethod
    def filter_by_baja(baja: BajaInventario) -> QuerySet[HistorialBaja]:
        """Retorna el historial de una baja específica."""
        return HistorialBaja.objects.filter(
            baja=baja,
            eliminado=False
        ).select_related(
            'estado_anterior', 'estado_nuevo', 'usuario'
        ).order_by('-fecha_cambio')

    @staticmethod
    def get_by_id(historial_id: int) -> Optional[HistorialBaja]:
        """Obtiene un registro de historial por su ID."""
        try:
            return HistorialBaja.objects.select_related(
                'baja', 'estado_anterior', 'estado_nuevo', 'usuario'
            ).get(id=historial_id, eliminado=False)
        except HistorialBaja.DoesNotExist:
            return None

    @staticmethod
    def create(
        baja: BajaInventario,
        estado_anterior: Optional[EstadoBaja],
        estado_nuevo: EstadoBaja,
        usuario: User,
        observaciones: str = ''
    ) -> HistorialBaja:
        """Crea un nuevo registro de historial."""
        return HistorialBaja.objects.create(
            baja=baja,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            usuario=usuario,
            observaciones=observaciones
        )
