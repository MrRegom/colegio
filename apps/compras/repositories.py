"""
Repository Pattern para el módulo de compras.

Separa la lógica de acceso a datos de la lógica de negocio,
siguiendo el principio de Inversión de Dependencias (SOLID).
"""
from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet, Q, Sum
from django.contrib.auth.models import User
from .models import (
    Proveedor, EstadoOrdenCompra, OrdenCompra,
    DetalleOrdenCompra, DetalleOrdenCompraArticulo,
    EstadoRecepcion, RecepcionArticulo, DetalleRecepcionArticulo,
    RecepcionActivo, DetalleRecepcionActivo
)
from apps.bodega.models import Bodega, Articulo
from apps.activos.models import Activo


# ==================== PROVEEDOR REPOSITORY ====================

class ProveedorRepository:
    """Repository para gestionar acceso a datos de Proveedor."""

    @staticmethod
    def get_all() -> QuerySet[Proveedor]:
        """Retorna todos los proveedores no eliminados."""
        return Proveedor.objects.filter(eliminado=False).order_by('razon_social')

    @staticmethod
    def get_active() -> QuerySet[Proveedor]:
        """Retorna solo proveedores activos y no eliminados."""
        return Proveedor.objects.filter(
            activo=True, eliminado=False
        ).order_by('razon_social')

    @staticmethod
    def get_by_id(proveedor_id: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por su ID."""
        try:
            return Proveedor.objects.get(id=proveedor_id, eliminado=False)
        except Proveedor.DoesNotExist:
            return None

    @staticmethod
    def get_by_rut(rut: str) -> Optional[Proveedor]:
        """Obtiene un proveedor por su RUT."""
        try:
            return Proveedor.objects.get(rut=rut, eliminado=False)
        except Proveedor.DoesNotExist:
            return None

    @staticmethod
    def search(query: str) -> QuerySet[Proveedor]:
        """Búsqueda de proveedores por RUT, razón social o nombre fantasía."""
        return Proveedor.objects.filter(
            Q(rut__icontains=query) |
            Q(razon_social__icontains=query) |
            Q(nombre_fantasia__icontains=query),
            eliminado=False
        ).order_by('razon_social')

    @staticmethod
    def exists_by_rut(rut: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe un proveedor con el RUT dado."""
        queryset = Proveedor.objects.filter(rut=rut)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()


# ==================== ESTADO ORDEN COMPRA REPOSITORY ====================

class EstadoOrdenCompraRepository:
    """Repository para gestionar estados de órdenes de compra."""

    @staticmethod
    def get_all() -> QuerySet[EstadoOrdenCompra]:
        """Retorna todos los estados activos."""
        return EstadoOrdenCompra.objects.filter(activo=True).order_by('codigo')

    @staticmethod
    def get_by_id(estado_id: int) -> Optional[EstadoOrdenCompra]:
        """Obtiene un estado por su ID."""
        try:
            return EstadoOrdenCompra.objects.get(id=estado_id, activo=True)
        except EstadoOrdenCompra.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[EstadoOrdenCompra]:
        """Obtiene un estado por su código."""
        try:
            return EstadoOrdenCompra.objects.get(codigo=codigo, activo=True)
        except EstadoOrdenCompra.DoesNotExist:
            return None

    @staticmethod
    def get_inicial() -> Optional[EstadoOrdenCompra]:
        """Obtiene el estado inicial del sistema (primer estado activo)."""
        return EstadoOrdenCompra.objects.filter(
            activo=True
        ).order_by('codigo').first()


# ==================== ORDEN COMPRA REPOSITORY ====================

class OrdenCompraRepository:
    """Repository para gestionar órdenes de compra."""

    @staticmethod
    def get_all() -> QuerySet[OrdenCompra]:
        """Retorna todas las órdenes con relaciones optimizadas."""
        return OrdenCompra.objects.select_related(
            'proveedor', 'bodega_destino', 'estado', 'solicitante', 'aprobador'
        ).order_by('-fecha_orden', '-numero')

    @staticmethod
    def get_by_id(orden_id: int) -> Optional[OrdenCompra]:
        """Obtiene una orden por su ID."""
        try:
            return OrdenCompra.objects.select_related(
                'proveedor', 'bodega_destino', 'estado', 'solicitante', 'aprobador'
            ).get(id=orden_id)
        except OrdenCompra.DoesNotExist:
            return None

    @staticmethod
    def get_by_numero(numero: str) -> Optional[OrdenCompra]:
        """Obtiene una orden por su número."""
        try:
            return OrdenCompra.objects.select_related(
                'proveedor', 'bodega_destino', 'estado', 'solicitante', 'aprobador'
            ).get(numero=numero)
        except OrdenCompra.DoesNotExist:
            return None

    @staticmethod
    def filter_by_proveedor(proveedor: Proveedor) -> QuerySet[OrdenCompra]:
        """Retorna órdenes de un proveedor específico."""
        return OrdenCompra.objects.filter(
            proveedor=proveedor
        ).select_related(
            'bodega_destino', 'estado', 'solicitante'
        ).order_by('-fecha_orden')

    @staticmethod
    def filter_by_estado(estado: EstadoOrdenCompra) -> QuerySet[OrdenCompra]:
        """Retorna órdenes en un estado específico."""
        return OrdenCompra.objects.filter(
            estado=estado
        ).select_related(
            'proveedor', 'bodega_destino', 'solicitante'
        ).order_by('-fecha_orden')

    @staticmethod
    def filter_by_solicitante(solicitante: User) -> QuerySet[OrdenCompra]:
        """Retorna órdenes solicitadas por un usuario."""
        return OrdenCompra.objects.filter(
            solicitante=solicitante
        ).select_related(
            'proveedor', 'bodega_destino', 'estado'
        ).order_by('-fecha_orden')

    @staticmethod
    def exists_by_numero(numero: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe una orden con el número dado."""
        queryset = OrdenCompra.objects.filter(numero=numero)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    @staticmethod
    def search(query: str) -> QuerySet[OrdenCompra]:
        """Búsqueda de órdenes por número o proveedor."""
        return OrdenCompra.objects.filter(
            Q(numero__icontains=query) |
            Q(proveedor__razon_social__icontains=query)
        ).select_related(
            'proveedor', 'bodega_destino', 'estado', 'solicitante'
        ).order_by('-fecha_orden')


# ==================== DETALLE ORDEN COMPRA REPOSITORIES ====================

class DetalleOrdenCompraRepository:
    """Repository para detalles de órdenes de compra (Activos)."""

    @staticmethod
    def filter_by_orden(orden: OrdenCompra) -> QuerySet[DetalleOrdenCompra]:
        """Retorna detalles de una orden específica."""
        return DetalleOrdenCompra.objects.filter(
            orden_compra=orden,
            eliminado=False
        ).select_related('activo').order_by('id')

    @staticmethod
    def get_by_id(detalle_id: int) -> Optional[DetalleOrdenCompra]:
        """Obtiene un detalle por su ID."""
        try:
            return DetalleOrdenCompra.objects.select_related(
                'orden_compra', 'activo'
            ).get(id=detalle_id, eliminado=False)
        except DetalleOrdenCompra.DoesNotExist:
            return None


class DetalleOrdenCompraArticuloRepository:
    """Repository para detalles de órdenes de compra (Artículos)."""

    @staticmethod
    def filter_by_orden(orden: OrdenCompra) -> QuerySet[DetalleOrdenCompraArticulo]:
        """Retorna detalles de una orden específica."""
        return DetalleOrdenCompraArticulo.objects.filter(
            orden_compra=orden,
            eliminado=False
        ).select_related('articulo').order_by('id')

    @staticmethod
    def get_by_id(detalle_id: int) -> Optional[DetalleOrdenCompraArticulo]:
        """Obtiene un detalle por su ID."""
        try:
            return DetalleOrdenCompraArticulo.objects.select_related(
                'orden_compra', 'articulo'
            ).get(id=detalle_id, eliminado=False)
        except DetalleOrdenCompraArticulo.DoesNotExist:
            return None


# ==================== ESTADO RECEPCIÓN REPOSITORY ====================

class EstadoRecepcionRepository:
    """Repository para estados de recepción."""

    @staticmethod
    def get_all() -> QuerySet[EstadoRecepcion]:
        """Retorna todos los estados no eliminados."""
        return EstadoRecepcion.objects.filter(
            eliminado=False, activo=True
        ).order_by('codigo')

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[EstadoRecepcion]:
        """Obtiene un estado por su código."""
        try:
            return EstadoRecepcion.objects.get(
                codigo=codigo, eliminado=False, activo=True
            )
        except EstadoRecepcion.DoesNotExist:
            return None

    @staticmethod
    def get_inicial() -> Optional[EstadoRecepcion]:
        """Obtiene el estado inicial (primer estado activo)."""
        return EstadoRecepcion.objects.filter(
            eliminado=False, activo=True
        ).order_by('codigo').first()


# ==================== RECEPCIÓN REPOSITORY BASE (DRY) ====================

class RecepcionRepositoryBase:
    """
    Repository base genérico para recepciones (artículos y activos).

    Principio DRY: Contiene todos los métodos comunes a ambos tipos de recepción.
    Las subclases solo necesitan definir el atributo 'model' y los métodos específicos.
    """
    model = None  # Debe ser sobrescrito por subclases

    @classmethod
    def get_all(cls) -> QuerySet:
        """Retorna todas las recepciones con relaciones optimizadas."""
        if not cls.model:
            raise NotImplementedError("Subclases deben definir el atributo 'model'")

        # RecepcionArticulo necesita bodega, RecepcionActivo no
        related_fields = ['orden_compra', 'estado', 'recibido_por']
        if hasattr(cls.model, '_meta') and any(f.name == 'bodega' for f in cls.model._meta.fields):
            related_fields.insert(1, 'bodega')

        return cls.model.objects.filter(
            eliminado=False
        ).select_related(*related_fields).order_by('-fecha_recepcion')

    @classmethod
    def get_by_id(cls, recepcion_id: int) -> Optional:
        """Obtiene una recepción por su ID."""
        if not cls.model:
            raise NotImplementedError("Subclases deben definir el atributo 'model'")

        try:
            related_fields = ['orden_compra', 'estado', 'recibido_por']
            if hasattr(cls.model, '_meta') and any(f.name == 'bodega' for f in cls.model._meta.fields):
                related_fields.insert(1, 'bodega')

            return cls.model.objects.select_related(*related_fields).get(
                id=recepcion_id, eliminado=False
            )
        except cls.model.DoesNotExist:
            return None

    @classmethod
    def get_by_numero(cls, numero: str) -> Optional:
        """Obtiene una recepción por su número."""
        if not cls.model:
            raise NotImplementedError("Subclases deben definir el atributo 'model'")

        try:
            related_fields = ['orden_compra', 'estado', 'recibido_por']
            if hasattr(cls.model, '_meta') and any(f.name == 'bodega' for f in cls.model._meta.fields):
                related_fields.insert(1, 'bodega')

            return cls.model.objects.select_related(*related_fields).get(
                numero=numero, eliminado=False
            )
        except cls.model.DoesNotExist:
            return None

    @classmethod
    def filter_by_orden(cls, orden: OrdenCompra) -> QuerySet:
        """Retorna recepciones de una orden específica."""
        if not cls.model:
            raise NotImplementedError("Subclases deben definir el atributo 'model'")

        related_fields = ['estado', 'recibido_por']
        if hasattr(cls.model, '_meta') and any(f.name == 'bodega' for f in cls.model._meta.fields):
            related_fields.insert(0, 'bodega')

        return cls.model.objects.filter(
            orden_compra=orden,
            eliminado=False
        ).select_related(*related_fields).order_by('-fecha_recepcion')

    @classmethod
    def filter_by_estado(cls, estado: EstadoRecepcion) -> QuerySet:
        """Retorna recepciones en un estado específico."""
        if not cls.model:
            raise NotImplementedError("Subclases deben definir el atributo 'model'")

        related_fields = ['orden_compra', 'recibido_por']
        if hasattr(cls.model, '_meta') and any(f.name == 'bodega' for f in cls.model._meta.fields):
            related_fields.insert(1, 'bodega')

        return cls.model.objects.filter(
            estado=estado,
            eliminado=False
        ).select_related(*related_fields).order_by('-fecha_recepcion')

    @classmethod
    def exists_by_numero(cls, numero: str, exclude_id: Optional[int] = None) -> bool:
        """Verifica si existe una recepción con el número dado."""
        if not cls.model:
            raise NotImplementedError("Subclases deben definir el atributo 'model'")

        queryset = cls.model.objects.filter(numero=numero)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()


# ==================== RECEPCIÓN ARTÍCULO REPOSITORY ====================

class RecepcionArticuloRepository(RecepcionRepositoryBase):
    """
    Repository para recepciones de artículos.
    Hereda métodos comunes de RecepcionRepositoryBase (DRY).
    """
    model = RecepcionArticulo  # Define el modelo específico

    @classmethod
    def filter_by_bodega(cls, bodega: Bodega) -> QuerySet[RecepcionArticulo]:
        """
        Retorna recepciones de una bodega específica.
        Método específico de artículos (los activos no tienen bodega).
        """
        return RecepcionArticulo.objects.filter(
            bodega=bodega,
            eliminado=False
        ).select_related('orden_compra', 'estado', 'recibido_por').order_by('-fecha_recepcion')


# ==================== DETALLE RECEPCIÓN ARTÍCULO REPOSITORY ====================

class DetalleRecepcionArticuloRepository:
    """Repository para detalles de recepciones de artículos."""

    @staticmethod
    def filter_by_recepcion(recepcion: RecepcionArticulo) -> QuerySet[DetalleRecepcionArticulo]:
        """Retorna detalles de una recepción específica."""
        return DetalleRecepcionArticulo.objects.filter(
            recepcion=recepcion,
            eliminado=False
        ).select_related('articulo').order_by('id')


# ==================== RECEPCIÓN ACTIVO REPOSITORY ====================

class RecepcionActivoRepository(RecepcionRepositoryBase):
    """
    Repository para recepciones de activos.
    Hereda todos los métodos de RecepcionRepositoryBase (DRY).
    No requiere métodos adicionales.
    """
    model = RecepcionActivo  # Define el modelo específico


# ==================== DETALLE RECEPCIÓN ACTIVO REPOSITORY ====================

class DetalleRecepcionActivoRepository:
    """Repository para detalles de recepciones de activos."""

    @staticmethod
    def filter_by_recepcion(recepcion: RecepcionActivo) -> QuerySet[DetalleRecepcionActivo]:
        """Retorna detalles de una recepción específica."""
        return DetalleRecepcionActivo.objects.filter(
            recepcion=recepcion,
            eliminado=False
        ).select_related('activo').order_by('id')
