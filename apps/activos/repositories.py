"""
Repository Pattern para el módulo de activos.

Implementa el patrón Repository de Clean Architecture para separar
la lógica de acceso a datos de la lógica de negocio, siguiendo
el principio de Inversión de Dependencias (SOLID).

Los repositories encapsulan las queries del ORM de Django y proporcionan
una interfaz limpia para el Service Layer.
"""
from __future__ import annotations

from typing import Optional

from django.db.models import QuerySet, Q
from django.contrib.auth.models import User

from .models import (
    CategoriaActivo, EstadoActivo, Ubicacion, Proveniencia,
    Marca, Taller, TipoMovimientoActivo, Activo, MovimientoActivo
)


# ==================== REPOSITORIOS DE CATÁLOGOS ====================

class CategoriaActivoRepository:
    """
    Repository para acceso a datos de CategoriaActivo.

    Encapsula todas las operaciones de consulta relacionadas con categorías.
    """

    @staticmethod
    def get_all() -> QuerySet[CategoriaActivo]:
        """Retorna todas las categorías no eliminadas."""
        return CategoriaActivo.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[CategoriaActivo]:
        """Retorna solo categorías activas y no eliminadas."""
        return CategoriaActivo.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(categoria_id: int) -> Optional[CategoriaActivo]:
        """Obtiene una categoría por su ID."""
        try:
            return CategoriaActivo.objects.get(id=categoria_id, eliminado=False)
        except CategoriaActivo.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[CategoriaActivo]:
        """Obtiene una categoría por su código."""
        try:
            return CategoriaActivo.objects.get(codigo=codigo, eliminado=False)
        except CategoriaActivo.DoesNotExist:
            return None

    @staticmethod
    def search(query: str) -> QuerySet[CategoriaActivo]:
        """Búsqueda de categorías por código o nombre."""
        return CategoriaActivo.objects.filter(
            Q(codigo__icontains=query) | Q(nombre__icontains=query),
            eliminado=False
        ).order_by('codigo')


class EstadoActivoRepository:
    """
    Repository para acceso a datos de EstadoActivo.

    Encapsula todas las operaciones de consulta relacionadas con estados.
    """

    @staticmethod
    def get_all() -> QuerySet[EstadoActivo]:
        """Retorna todos los estados no eliminados."""
        return EstadoActivo.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[EstadoActivo]:
        """Retorna solo estados activos y no eliminados."""
        return EstadoActivo.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(estado_id: int) -> Optional[EstadoActivo]:
        """Obtiene un estado por su ID."""
        try:
            return EstadoActivo.objects.get(id=estado_id, eliminado=False)
        except EstadoActivo.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[EstadoActivo]:
        """Obtiene un estado por su código."""
        try:
            return EstadoActivo.objects.get(codigo=codigo, eliminado=False)
        except EstadoActivo.DoesNotExist:
            return None

    @staticmethod
    def get_inicial() -> Optional[EstadoActivo]:
        """Obtiene el estado inicial del sistema."""
        return EstadoActivo.objects.filter(
            es_inicial=True, activo=True, eliminado=False
        ).first()


class UbicacionRepository:
    """
    Repository para acceso a datos de Ubicacion.

    Encapsula todas las operaciones de consulta relacionadas con ubicaciones.
    """

    @staticmethod
    def get_all() -> QuerySet[Ubicacion]:
        """Retorna todas las ubicaciones no eliminadas."""
        return Ubicacion.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[Ubicacion]:
        """Retorna solo ubicaciones activas y no eliminadas."""
        return Ubicacion.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(ubicacion_id: int) -> Optional[Ubicacion]:
        """Obtiene una ubicación por su ID."""
        try:
            return Ubicacion.objects.get(id=ubicacion_id, eliminado=False)
        except Ubicacion.DoesNotExist:
            return None

    @staticmethod
    def search(query: str) -> QuerySet[Ubicacion]:
        """Búsqueda de ubicaciones por código o nombre."""
        return Ubicacion.objects.filter(
            Q(codigo__icontains=query) | Q(nombre__icontains=query),
            eliminado=False
        ).order_by('codigo')


class ProvenienciaRepository:
    """Repository para acceso a datos de Proveniencia."""

    @staticmethod
    def get_all() -> QuerySet[Proveniencia]:
        """Retorna todas las proveniencias no eliminadas."""
        return Proveniencia.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[Proveniencia]:
        """Retorna solo proveniencias activas."""
        return Proveniencia.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(proveniencia_id: int) -> Optional[Proveniencia]:
        """Obtiene una proveniencia por su ID."""
        try:
            return Proveniencia.objects.get(id=proveniencia_id, eliminado=False)
        except Proveniencia.DoesNotExist:
            return None


class MarcaRepository:
    """Repository para acceso a datos de Marca."""

    @staticmethod
    def get_all() -> QuerySet[Marca]:
        """Retorna todas las marcas no eliminadas."""
        return Marca.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[Marca]:
        """Retorna solo marcas activas."""
        return Marca.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(marca_id: int) -> Optional[Marca]:
        """Obtiene una marca por su ID."""
        try:
            return Marca.objects.get(id=marca_id, eliminado=False)
        except Marca.DoesNotExist:
            return None


class TallerRepository:
    """Repository para acceso a datos de Taller."""

    @staticmethod
    def get_all() -> QuerySet[Taller]:
        """Retorna todos los talleres no eliminados."""
        return Taller.objects.filter(eliminado=False).select_related(
            'responsable'
        ).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[Taller]:
        """Retorna solo talleres activos."""
        return Taller.objects.filter(
            activo=True, eliminado=False
        ).select_related('responsable').order_by('codigo')

    @staticmethod
    def get_by_id(taller_id: int) -> Optional[Taller]:
        """Obtiene un taller por su ID."""
        try:
            return Taller.objects.select_related('responsable').get(
                id=taller_id, eliminado=False
            )
        except Taller.DoesNotExist:
            return None


class TipoMovimientoActivoRepository:
    """Repository para acceso a datos de TipoMovimientoActivo."""

    @staticmethod
    def get_all() -> QuerySet[TipoMovimientoActivo]:
        """Retorna todos los tipos de movimiento no eliminados."""
        return TipoMovimientoActivo.objects.filter(
            eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[TipoMovimientoActivo]:
        """Retorna solo tipos activos y no eliminados."""
        return TipoMovimientoActivo.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(tipo_id: int) -> Optional[TipoMovimientoActivo]:
        """Obtiene un tipo de movimiento por su ID."""
        try:
            return TipoMovimientoActivo.objects.get(
                id=tipo_id, eliminado=False
            )
        except TipoMovimientoActivo.DoesNotExist:
            return None


# ==================== ACTIVO REPOSITORY ====================

class ActivoRepository:
    """
    Repository para acceso a datos de Activo.

    Encapsula todas las operaciones de consulta relacionadas con activos,
    optimizando las queries con select_related para evitar N+1.
    """

    @staticmethod
    def get_all() -> QuerySet[Activo]:
        """Retorna todos los activos no eliminados con relaciones optimizadas."""
        return Activo.objects.filter(eliminado=False).select_related(
            'categoria', 'estado', 'marca'
        ).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[Activo]:
        """Retorna solo activos activos y no eliminados."""
        return Activo.objects.filter(
            activo=True, eliminado=False
        ).select_related(
            'categoria', 'estado', 'marca'
        ).order_by('codigo')

    @staticmethod
    def get_by_id(activo_id: int) -> Optional[Activo]:
        """Obtiene un activo por su ID."""
        try:
            return Activo.objects.select_related(
                'categoria', 'estado', 'marca'
            ).get(id=activo_id, eliminado=False)
        except Activo.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Activo]:
        """Obtiene un activo por su código."""
        try:
            return Activo.objects.select_related(
                'categoria', 'estado', 'marca'
            ).get(codigo=codigo, eliminado=False)
        except Activo.DoesNotExist:
            return None

    @staticmethod
    def filter_by_categoria(categoria: CategoriaActivo) -> QuerySet[Activo]:
        """Retorna activos de una categoría específica."""
        return Activo.objects.filter(
            categoria=categoria, eliminado=False
        ).select_related(
            'categoria', 'estado', 'marca'
        ).order_by('codigo')

    @staticmethod
    def filter_by_estado(estado: EstadoActivo) -> QuerySet[Activo]:
        """Retorna activos en un estado específico."""
        return Activo.objects.filter(
            estado=estado, eliminado=False
        ).select_related(
            'categoria', 'estado', 'marca'
        ).order_by('codigo')

    @staticmethod
    def search(query: str) -> QuerySet[Activo]:
        """Búsqueda de activos por código, nombre, número de serie o código de barras."""
        return Activo.objects.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(numero_serie__icontains=query) |
            Q(codigo_barras__icontains=query),
            eliminado=False
        ).select_related(
            'categoria', 'estado', 'marca'
        ).order_by('codigo')

    @staticmethod
    def exists_by_codigo(codigo: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe un activo con el código dado."""
        queryset = Activo.objects.filter(codigo=codigo)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    @staticmethod
    def create(**kwargs) -> Activo:
        """Crea un nuevo activo."""
        return Activo.objects.create(**kwargs)

    @staticmethod
    def update(activo: Activo, **kwargs) -> Activo:
        """Actualiza un activo existente."""
        for key, value in kwargs.items():
            setattr(activo, key, value)
        activo.save()
        return activo


# ==================== MOVIMIENTO ACTIVO REPOSITORY ====================

class MovimientoActivoRepository:
    """
    Repository para acceso a datos de MovimientoActivo.

    Encapsula todas las operaciones de consulta relacionadas con movimientos,
    optimizando las queries con select_related.
    """

    @staticmethod
    def get_all() -> QuerySet[MovimientoActivo]:
        """Retorna todos los movimientos con relaciones optimizadas."""
        return MovimientoActivo.objects.filter(eliminado=False).select_related(
            'activo', 'tipo_movimiento', 'ubicacion_destino',
            'taller', 'responsable', 'proveniencia', 'usuario_registro'
        ).order_by('-fecha_creacion')

    @staticmethod
    def get_by_id(movimiento_id: int) -> Optional[MovimientoActivo]:
        """Obtiene un movimiento por su ID."""
        try:
            return MovimientoActivo.objects.select_related(
                'activo', 'tipo_movimiento', 'ubicacion_destino',
                'taller', 'responsable', 'proveniencia', 'usuario_registro'
            ).get(id=movimiento_id, eliminado=False)
        except MovimientoActivo.DoesNotExist:
            return None

    @staticmethod
    def filter_by_activo(activo: Activo, limit: int = 20) -> QuerySet[MovimientoActivo]:
        """Retorna movimientos de un activo específico."""
        return MovimientoActivo.objects.filter(
            activo=activo, eliminado=False
        ).select_related(
            'tipo_movimiento', 'ubicacion_destino', 'taller',
            'responsable', 'proveniencia', 'usuario_registro'
        ).order_by('-fecha_creacion')[:limit]

    @staticmethod
    def filter_by_ubicacion(ubicacion: Ubicacion) -> QuerySet[MovimientoActivo]:
        """Retorna movimientos hacia una ubicación específica."""
        return MovimientoActivo.objects.filter(
            ubicacion_destino=ubicacion, eliminado=False
        ).select_related(
            'activo', 'tipo_movimiento', 'taller',
            'responsable', 'proveniencia', 'usuario_registro'
        ).order_by('-fecha_creacion')

    @staticmethod
    def filter_by_responsable(responsable: User) -> QuerySet[MovimientoActivo]:
        """Retorna movimientos de un responsable específico."""
        return MovimientoActivo.objects.filter(
            responsable=responsable, eliminado=False
        ).select_related(
            'activo', 'tipo_movimiento', 'ubicacion_destino',
            'taller', 'proveniencia', 'usuario_registro'
        ).order_by('-fecha_creacion')

    @staticmethod
    def create(**kwargs) -> MovimientoActivo:
        """Crea un nuevo movimiento."""
        return MovimientoActivo.objects.create(**kwargs)

    @staticmethod
    def get_ultimo_por_activo(activo: Activo) -> Optional[MovimientoActivo]:
        """Obtiene el último movimiento de un activo."""
        return MovimientoActivo.objects.filter(
            activo=activo, eliminado=False
        ).select_related(
            'ubicacion_destino', 'responsable'
        ).order_by('-fecha_creacion').first()
