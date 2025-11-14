"""
Repository Pattern para el módulo de bodega.

Separa la lógica de acceso a datos de la lógica de negocio,
siguiendo el principio de Inversión de Dependencias (SOLID).
"""
from typing import Optional, List
from decimal import Decimal
from django.db.models import QuerySet, Q
from django.contrib.auth.models import User
from .models import (
    Bodega, Categoria, Articulo, TipoMovimiento, Movimiento,
    EstadoEntrega, TipoEntrega, EntregaArticulo, DetalleEntregaArticulo,
    EntregaBien, DetalleEntregaBien
)


# ==================== BODEGA REPOSITORY ====================

class BodegaRepository:
    """Repository para gestionar acceso a datos de Bodega."""

    @staticmethod
    def get_all() -> QuerySet[Bodega]:
        """Retorna todas las bodegas no eliminadas."""
        return Bodega.objects.filter(eliminado=False)

    @staticmethod
    def get_active() -> QuerySet[Bodega]:
        """Retorna solo bodegas activas y no eliminadas."""
        return Bodega.objects.filter(activo=True, eliminado=False)

    @staticmethod
    def get_by_id(bodega_id: int) -> Optional[Bodega]:
        """
        Obtiene una bodega por su ID.

        Args:
            bodega_id: ID de la bodega

        Returns:
            Bodega si existe, None en caso contrario
        """
        try:
            return Bodega.objects.get(id=bodega_id, eliminado=False)
        except Bodega.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Bodega]:
        """
        Obtiene una bodega por su código.

        Args:
            codigo: Código único de la bodega

        Returns:
            Bodega si existe, None en caso contrario
        """
        try:
            return Bodega.objects.get(codigo=codigo, eliminado=False)
        except Bodega.DoesNotExist:
            return None

    @staticmethod
    def filter_by_responsable(responsable: User) -> QuerySet[Bodega]:
        """Retorna bodegas gestionadas por un responsable específico."""
        return Bodega.objects.filter(
            responsable=responsable,
            eliminado=False
        )

    @staticmethod
    def search(query: str) -> QuerySet[Bodega]:
        """
        Búsqueda de bodegas por código o nombre.

        Args:
            query: Término de búsqueda

        Returns:
            QuerySet con resultados
        """
        return Bodega.objects.filter(
            Q(codigo__icontains=query) | Q(nombre__icontains=query),
            eliminado=False
        )


# ==================== CATEGORÍA REPOSITORY ====================

class CategoriaRepository:
    """Repository para gestionar acceso a datos de Categoría."""

    @staticmethod
    def get_all() -> QuerySet[Categoria]:
        """Retorna todas las categorías no eliminadas."""
        return Categoria.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[Categoria]:
        """Retorna solo categorías activas y no eliminadas."""
        return Categoria.objects.filter(activo=True, eliminado=False).order_by('codigo')

    @staticmethod
    def get_by_id(categoria_id: int) -> Optional[Categoria]:
        """
        Obtiene una categoría por su ID.

        Args:
            categoria_id: ID de la categoría

        Returns:
            Categoría si existe, None en caso contrario
        """
        try:
            return Categoria.objects.get(id=categoria_id, eliminado=False)
        except Categoria.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Categoria]:
        """
        Obtiene una categoría por su código.

        Args:
            codigo: Código único de la categoría

        Returns:
            Categoría si existe, None en caso contrario
        """
        try:
            return Categoria.objects.get(codigo=codigo, eliminado=False)
        except Categoria.DoesNotExist:
            return None

    @staticmethod
    def search(query: str) -> QuerySet[Categoria]:
        """
        Búsqueda de categorías por código o nombre.

        Args:
            query: Término de búsqueda

        Returns:
            QuerySet con resultados
        """
        return Categoria.objects.filter(
            Q(codigo__icontains=query) | Q(nombre__icontains=query),
            eliminado=False
        ).order_by('codigo')

    @staticmethod
    def exists_by_codigo(codigo: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe una categoría con el código dado.

        Args:
            codigo: Código a verificar
            exclude_id: ID a excluir de la búsqueda (para ediciones)

        Returns:
            True si existe, False en caso contrario
        """
        queryset = Categoria.objects.filter(codigo=codigo)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()


# ==================== ARTÍCULO REPOSITORY ====================

class ArticuloRepository:
    """Repository para gestionar acceso a datos de Artículo."""

    @staticmethod
    def get_all() -> QuerySet[Articulo]:
        """Retorna todos los artículos no eliminados con relaciones optimizadas."""
        return Articulo.objects.filter(
            eliminado=False
        ).select_related(
            'categoria', 'ubicacion_fisica'
        ).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[Articulo]:
        """Retorna solo artículos activos y no eliminados."""
        return Articulo.objects.filter(
            activo=True, eliminado=False
        ).select_related(
            'categoria', 'ubicacion_fisica'
        ).order_by('codigo')

    @staticmethod
    def get_by_id(articulo_id: int) -> Optional[Articulo]:
        """
        Obtiene un artículo por su ID.

        Args:
            articulo_id: ID del artículo

        Returns:
            Artículo si existe, None en caso contrario
        """
        try:
            return Articulo.objects.select_related(
                'categoria', 'ubicacion_fisica'
            ).get(id=articulo_id, eliminado=False)
        except Articulo.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[Articulo]:
        """
        Obtiene un artículo por su código.

        Args:
            codigo: Código único del artículo

        Returns:
            Artículo si existe, None en caso contrario
        """
        try:
            return Articulo.objects.select_related(
                'categoria', 'ubicacion_fisica'
            ).get(codigo=codigo, eliminado=False)
        except Articulo.DoesNotExist:
            return None

    @staticmethod
    def filter_by_categoria(categoria: Categoria) -> QuerySet[Articulo]:
        """Retorna artículos de una categoría específica."""
        return Articulo.objects.filter(
            categoria=categoria,
            eliminado=False
        ).select_related(
            'categoria', 'ubicacion_fisica'
        ).order_by('codigo')

    @staticmethod
    def filter_by_bodega(bodega: Bodega) -> QuerySet[Articulo]:
        """Retorna artículos de una bodega específica."""
        return Articulo.objects.filter(
            ubicacion_fisica=bodega,
            eliminado=False
        ).select_related(
            'categoria', 'ubicacion_fisica'
        ).order_by('codigo')

    @staticmethod
    def get_low_stock() -> QuerySet[Articulo]:
        """Retorna artículos con stock bajo (menor al mínimo)."""
        from django.db.models import F
        return Articulo.objects.filter(
            eliminado=False,
            activo=True
        ).filter(
            stock_actual__lt=F('stock_minimo')
        ).select_related(
            'categoria', 'ubicacion_fisica'
        ).order_by('codigo')

    @staticmethod
    def get_reorder_point() -> QuerySet[Articulo]:
        """Retorna artículos que alcanzaron el punto de reorden."""
        from django.db.models import F
        return Articulo.objects.filter(
            eliminado=False,
            activo=True,
            punto_reorden__isnull=False
        ).filter(
            stock_actual__lte=F('punto_reorden')
        ).select_related(
            'categoria', 'ubicacion_fisica'
        ).order_by('codigo')

    @staticmethod
    def search(query: str) -> QuerySet[Articulo]:
        """
        Búsqueda de artículos por código, nombre o descripción.

        Args:
            query: Término de búsqueda

        Returns:
            QuerySet con resultados
        """
        return Articulo.objects.filter(
            Q(codigo__icontains=query) |
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query),
            eliminado=False
        ).select_related(
            'categoria', 'ubicacion_fisica'
        ).order_by('codigo')

    @staticmethod
    def exists_by_codigo(codigo: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un artículo con el código dado.

        Args:
            codigo: Código a verificar
            exclude_id: ID a excluir de la búsqueda (para ediciones)

        Returns:
            True si existe, False en caso contrario
        """
        queryset = Articulo.objects.filter(codigo=codigo)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    @staticmethod
    def update_stock(articulo: Articulo, nuevo_stock: Decimal) -> Articulo:
        """
        Actualiza el stock de un artículo.

        Args:
            articulo: Artículo a actualizar
            nuevo_stock: Nuevo valor de stock

        Returns:
            Artículo actualizado
        """
        articulo.stock_actual = nuevo_stock
        articulo.save(update_fields=['stock_actual', 'fecha_actualizacion'])
        return articulo


# ==================== TIPO MOVIMIENTO REPOSITORY ====================

class TipoMovimientoRepository:
    """Repository para gestionar acceso a datos de TipoMovimiento."""

    @staticmethod
    def get_all() -> QuerySet[TipoMovimiento]:
        """Retorna todos los tipos de movimiento no eliminados."""
        return TipoMovimiento.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[TipoMovimiento]:
        """Retorna solo tipos de movimiento activos y no eliminados."""
        return TipoMovimiento.objects.filter(
            activo=True, eliminado=False
        ).order_by('codigo')

    @staticmethod
    def get_by_id(tipo_id: int) -> Optional[TipoMovimiento]:
        """
        Obtiene un tipo de movimiento por su ID.

        Args:
            tipo_id: ID del tipo de movimiento

        Returns:
            TipoMovimiento si existe, None en caso contrario
        """
        try:
            return TipoMovimiento.objects.get(id=tipo_id, eliminado=False)
        except TipoMovimiento.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[TipoMovimiento]:
        """
        Obtiene un tipo de movimiento por su código.

        Args:
            codigo: Código único del tipo de movimiento

        Returns:
            TipoMovimiento si existe, None en caso contrario
        """
        try:
            return TipoMovimiento.objects.get(codigo=codigo, eliminado=False)
        except TipoMovimiento.DoesNotExist:
            return None


# ==================== MOVIMIENTO REPOSITORY ====================

class MovimientoRepository:
    """Repository para gestionar acceso a datos de Movimiento."""

    @staticmethod
    def get_all() -> QuerySet[Movimiento]:
        """Retorna todos los movimientos no eliminados con relaciones optimizadas."""
        return Movimiento.objects.filter(
            eliminado=False
        ).select_related(
            'articulo', 'tipo', 'usuario'
        ).order_by('-fecha_creacion')

    @staticmethod
    def get_by_id(movimiento_id: int) -> Optional[Movimiento]:
        """
        Obtiene un movimiento por su ID.

        Args:
            movimiento_id: ID del movimiento

        Returns:
            Movimiento si existe, None en caso contrario
        """
        try:
            return Movimiento.objects.select_related(
                'articulo', 'tipo', 'usuario'
            ).get(id=movimiento_id, eliminado=False)
        except Movimiento.DoesNotExist:
            return None

    @staticmethod
    def filter_by_articulo(articulo: Articulo, limit: int = 20) -> QuerySet[Movimiento]:
        """
        Retorna movimientos de un artículo específico.

        Args:
            articulo: Artículo a filtrar
            limit: Número máximo de resultados

        Returns:
            QuerySet con movimientos limitados
        """
        return Movimiento.objects.filter(
            articulo=articulo,
            eliminado=False
        ).select_related(
            'tipo', 'usuario'
        ).order_by('-fecha_creacion')[:limit]

    @staticmethod
    def filter_by_tipo(tipo: TipoMovimiento) -> QuerySet[Movimiento]:
        """Retorna movimientos de un tipo específico."""
        return Movimiento.objects.filter(
            tipo=tipo,
            eliminado=False
        ).select_related(
            'articulo', 'usuario'
        ).order_by('-fecha_creacion')

    @staticmethod
    def filter_by_operacion(operacion: str) -> QuerySet[Movimiento]:
        """
        Retorna movimientos de una operación específica.

        Args:
            operacion: 'ENTRADA' o 'SALIDA'

        Returns:
            QuerySet con movimientos filtrados
        """
        return Movimiento.objects.filter(
            operacion=operacion,
            eliminado=False
        ).select_related(
            'articulo', 'tipo', 'usuario'
        ).order_by('-fecha_creacion')

    @staticmethod
    def filter_by_usuario(usuario: User) -> QuerySet[Movimiento]:
        """Retorna movimientos realizados por un usuario específico."""
        return Movimiento.objects.filter(
            usuario=usuario,
            eliminado=False
        ).select_related(
            'articulo', 'tipo'
        ).order_by('-fecha_creacion')

    @staticmethod
    def create(
        articulo: Articulo,
        tipo: TipoMovimiento,
        cantidad: Decimal,
        operacion: str,
        usuario: User,
        motivo: str,
        stock_antes: Decimal,
        stock_despues: Decimal
    ) -> Movimiento:
        """
        Crea un nuevo movimiento.

        Args:
            articulo: Artículo del movimiento
            tipo: Tipo de movimiento
            cantidad: Cantidad movida
            operacion: 'ENTRADA' o 'SALIDA'
            usuario: Usuario que realiza el movimiento
            motivo: Motivo del movimiento
            stock_antes: Stock anterior
            stock_despues: Stock posterior

        Returns:
            Movimiento creado
        """
        return Movimiento.objects.create(
            articulo=articulo,
            tipo=tipo,
            cantidad=cantidad,
            operacion=operacion,
            usuario=usuario,
            motivo=motivo,
            stock_antes=stock_antes,
            stock_despues=stock_despues
        )


# ==================== ENTREGA REPOSITORIES ====================

class EstadoEntregaRepository:
    """Repository para gestionar acceso a datos de EstadoEntrega."""

    @staticmethod
    def get_all() -> QuerySet[EstadoEntrega]:
        """Retorna todos los estados de entrega no eliminados."""
        return EstadoEntrega.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[EstadoEntrega]:
        """Retorna solo estados de entrega activos."""
        return EstadoEntrega.objects.filter(activo=True, eliminado=False).order_by('codigo')

    @staticmethod
    def get_by_id(estado_id: int) -> Optional[EstadoEntrega]:
        """Obtiene un estado de entrega por su ID."""
        try:
            return EstadoEntrega.objects.get(id=estado_id, eliminado=False)
        except EstadoEntrega.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[EstadoEntrega]:
        """Obtiene un estado de entrega por su código."""
        try:
            return EstadoEntrega.objects.get(codigo=codigo, eliminado=False)
        except EstadoEntrega.DoesNotExist:
            return None

    @staticmethod
    def get_inicial() -> Optional[EstadoEntrega]:
        """Obtiene el estado inicial de entrega."""
        try:
            return EstadoEntrega.objects.get(es_inicial=True, eliminado=False)
        except EstadoEntrega.DoesNotExist:
            return None


class TipoEntregaRepository:
    """Repository para gestionar acceso a datos de TipoEntrega."""

    @staticmethod
    def get_all() -> QuerySet[TipoEntrega]:
        """Retorna todos los tipos de entrega no eliminados."""
        return TipoEntrega.objects.filter(eliminado=False).order_by('codigo')

    @staticmethod
    def get_active() -> QuerySet[TipoEntrega]:
        """Retorna solo tipos de entrega activos."""
        return TipoEntrega.objects.filter(activo=True, eliminado=False).order_by('codigo')

    @staticmethod
    def get_by_id(tipo_id: int) -> Optional[TipoEntrega]:
        """Obtiene un tipo de entrega por su ID."""
        try:
            return TipoEntrega.objects.get(id=tipo_id, eliminado=False)
        except TipoEntrega.DoesNotExist:
            return None

    @staticmethod
    def get_by_codigo(codigo: str) -> Optional[TipoEntrega]:
        """Obtiene un tipo de entrega por su código."""
        try:
            return TipoEntrega.objects.get(codigo=codigo, eliminado=False)
        except TipoEntrega.DoesNotExist:
            return None


class EntregaArticuloRepository:
    """Repository para gestionar acceso a datos de EntregaArticulo."""

    @staticmethod
    def get_all() -> QuerySet[EntregaArticulo]:
        """Retorna todas las entregas de artículos con relaciones optimizadas."""
        return EntregaArticulo.objects.filter(
            eliminado=False
        ).select_related(
            'tipo', 'estado', 'entregado_por', 'bodega_origen'
        ).prefetch_related('detalles__articulo').order_by('-fecha_entrega')

    @staticmethod
    def get_by_id(entrega_id: int) -> Optional[EntregaArticulo]:
        """Obtiene una entrega de artículo por su ID."""
        try:
            return EntregaArticulo.objects.select_related(
                'tipo', 'estado', 'entregado_por', 'bodega_origen'
            ).prefetch_related('detalles__articulo').get(id=entrega_id, eliminado=False)
        except EntregaArticulo.DoesNotExist:
            return None

    @staticmethod
    def get_by_numero(numero: str) -> Optional[EntregaArticulo]:
        """Obtiene una entrega de artículo por su número."""
        try:
            return EntregaArticulo.objects.select_related(
                'tipo', 'estado', 'entregado_por', 'bodega_origen'
            ).get(numero=numero, eliminado=False)
        except EntregaArticulo.DoesNotExist:
            return None

    @staticmethod
    def filter_by_bodega(bodega: Bodega) -> QuerySet[EntregaArticulo]:
        """Retorna entregas de una bodega específica."""
        return EntregaArticulo.objects.filter(
            bodega_origen=bodega,
            eliminado=False
        ).select_related(
            'tipo', 'estado', 'entregado_por'
        ).order_by('-fecha_entrega')

    @staticmethod
    def filter_by_estado(estado: EstadoEntrega) -> QuerySet[EntregaArticulo]:
        """Retorna entregas con un estado específico."""
        return EntregaArticulo.objects.filter(
            estado=estado,
            eliminado=False
        ).select_related(
            'tipo', 'bodega_origen', 'entregado_por'
        ).order_by('-fecha_entrega')

    @staticmethod
    def search(query: str) -> QuerySet[EntregaArticulo]:
        """Búsqueda de entregas por número o receptor."""
        return EntregaArticulo.objects.filter(
            Q(numero__icontains=query) |
            Q(recibido_por__first_name__icontains=query) |
            Q(recibido_por__last_name__icontains=query) |
            Q(recibido_por__username__icontains=query),
            eliminado=False
        ).select_related(
            'tipo', 'estado', 'entregado_por', 'bodega_origen', 'recibido_por'
        ).order_by('-fecha_entrega')


class DetalleEntregaArticuloRepository:
    """Repository para gestionar acceso a datos de DetalleEntregaArticulo."""

    @staticmethod
    def get_by_entrega(entrega: EntregaArticulo) -> QuerySet[DetalleEntregaArticulo]:
        """Retorna detalles de una entrega específica."""
        return DetalleEntregaArticulo.objects.filter(
            entrega=entrega,
            eliminado=False
        ).select_related('articulo').order_by('id')

    @staticmethod
    def filter_by_articulo(articulo: Articulo) -> QuerySet[DetalleEntregaArticulo]:
        """Retorna detalles de entregas de un artículo específico."""
        return DetalleEntregaArticulo.objects.filter(
            articulo=articulo,
            eliminado=False
        ).select_related('entrega').order_by('-entrega__fecha_entrega')


class EntregaBienRepository:
    """Repository para gestionar acceso a datos de EntregaBien."""

    @staticmethod
    def get_all() -> QuerySet[EntregaBien]:
        """Retorna todas las entregas de bienes con relaciones optimizadas."""
        return EntregaBien.objects.filter(
            eliminado=False
        ).select_related(
            'tipo', 'estado', 'entregado_por'
        ).prefetch_related('detalles__equipo').order_by('-fecha_entrega')

    @staticmethod
    def get_by_id(entrega_id: int) -> Optional[EntregaBien]:
        """Obtiene una entrega de bien por su ID."""
        try:
            return EntregaBien.objects.select_related(
                'tipo', 'estado', 'entregado_por'
            ).prefetch_related('detalles__equipo').get(id=entrega_id, eliminado=False)
        except EntregaBien.DoesNotExist:
            return None

    @staticmethod
    def get_by_numero(numero: str) -> Optional[EntregaBien]:
        """Obtiene una entrega de bien por su número."""
        try:
            return EntregaBien.objects.select_related(
                'tipo', 'estado', 'entregado_por'
            ).get(numero=numero, eliminado=False)
        except EntregaBien.DoesNotExist:
            return None

    @staticmethod
    def filter_by_estado(estado: EstadoEntrega) -> QuerySet[EntregaBien]:
        """Retorna entregas con un estado específico."""
        return EntregaBien.objects.filter(
            estado=estado,
            eliminado=False
        ).select_related(
            'tipo', 'entregado_por'
        ).order_by('-fecha_entrega')

    @staticmethod
    def search(query: str) -> QuerySet[EntregaBien]:
        """Búsqueda de entregas por número o receptor."""
        return EntregaBien.objects.filter(
            Q(numero__icontains=query) |
            Q(recibido_por__first_name__icontains=query) |
            Q(recibido_por__last_name__icontains=query) |
            Q(recibido_por__username__icontains=query),
            eliminado=False
        ).select_related(
            'tipo', 'estado', 'entregado_por', 'recibido_por'
        ).order_by('-fecha_entrega')


class DetalleEntregaBienRepository:
    """Repository para gestionar acceso a datos de DetalleEntregaBien."""

    @staticmethod
    def get_by_entrega(entrega: EntregaBien) -> QuerySet[DetalleEntregaBien]:
        """Retorna detalles de una entrega específica."""
        return DetalleEntregaBien.objects.filter(
            entrega=entrega,
            eliminado=False
        ).select_related('equipo').order_by('id')

    @staticmethod
    def filter_by_equipo(equipo) -> QuerySet[DetalleEntregaBien]:
        """Retorna detalles de entregas de un equipo específico."""
        return DetalleEntregaBien.objects.filter(
            equipo=equipo,
            eliminado=False
        ).select_related('entrega').order_by('-entrega__fecha_entrega')
