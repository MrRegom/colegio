"""
Service Layer para el módulo de activos.

Implementa el patrón Service Layer de Clean Architecture que contiene
la lógica de negocio y coordina los repositories, siguiendo el principio
de Single Responsibility (SOLID).

Los servicios orquestan operaciones complejas, validan reglas de negocio
y mantienen las transacciones atómicas cuando es necesario.
"""
from __future__ import annotations

from typing import Optional, Dict, Any, Tuple

from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import (
    CategoriaActivo, EstadoActivo, Ubicacion, Proveniencia,
    Marca, Taller, TipoMovimientoActivo, Activo, MovimientoActivo
)
from .repositories import (
    CategoriaActivoRepository, EstadoActivoRepository,
    UbicacionRepository, ProvenienciaRepository,
    MarcaRepository, TallerRepository,
    TipoMovimientoActivoRepository, ActivoRepository,
    MovimientoActivoRepository
)


# ==================== ACTIVO SERVICE ====================

class ActivoService:
    """
    Service para lógica de negocio de Activo.

    Coordina operaciones complejas y validaciones de negocio relacionadas
    con activos, siguiendo Clean Architecture.
    """

    def __init__(self) -> None:
        self.repository = ActivoRepository()
        self.estado_repo = EstadoActivoRepository()

    def crear_activo(
        self,
        codigo: str,
        nombre: str,
        categoria: CategoriaActivo,
        descripcion: Optional[str] = None,
        marca: Optional[Marca] = None,
        lote: Optional[str] = None,
        numero_serie: Optional[str] = None,
        codigo_barras: Optional[str] = None,
        precio_unitario: Optional[Decimal] = None
    ) -> Activo:
        """
        Crea un nuevo activo validando reglas de negocio.

        Args:
            codigo: Código único del activo
            nombre: Nombre del activo
            categoria: Categoría del activo
            descripcion: Descripción opcional
            marca: Marca opcional
            lote: Lote opcional
            numero_serie: Número de serie opcional
            codigo_barras: Código de barras (se auto-genera si no se proporciona)
            precio_unitario: Precio unitario opcional

        Returns:
            Activo creado

        Raises:
            ValidationError: Si el código ya existe o faltan campos requeridos
        """
        # Validar unicidad del código
        if self.repository.exists_by_codigo(codigo):
            raise ValidationError({
                'codigo': f'Ya existe un activo con el código "{codigo}".'
            })

        # Obtener estado inicial
        estado_inicial = self.estado_repo.get_inicial()
        if not estado_inicial:
            raise ValidationError({
                'estado': 'No existe un estado inicial configurado. '
                          'Configure un estado como inicial en el catálogo.'
            })

        # Normalizar datos
        codigo_normalizado = codigo.strip().upper()
        nombre_normalizado = nombre.strip()

        # Crear activo
        activo = self.repository.create(
            codigo=codigo_normalizado,
            nombre=nombre_normalizado,
            descripcion=descripcion,
            categoria=categoria,
            estado=estado_inicial,
            marca=marca,
            lote=lote,
            numero_serie=numero_serie,
            codigo_barras=codigo_barras,
            precio_unitario=precio_unitario
        )

        return activo

    def actualizar_activo(
        self,
        activo: Activo,
        datos: Dict[str, Any]
    ) -> Activo:
        """
        Actualiza un activo existente validando reglas de negocio.

        Args:
            activo: Activo a actualizar
            datos: Diccionario con los datos a actualizar

        Returns:
            Activo actualizado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar código si se está actualizando
        if 'codigo' in datos and datos['codigo'] != activo.codigo:
            if self.repository.exists_by_codigo(datos['codigo'], exclude_id=activo.id):
                raise ValidationError({
                    'codigo': f'Ya existe un activo con el código "{datos["codigo"]}".'
                })

        # Normalizar datos de texto
        if 'codigo' in datos and isinstance(datos['codigo'], str):
            datos['codigo'] = datos['codigo'].strip().upper()
        if 'nombre' in datos and isinstance(datos['nombre'], str):
            datos['nombre'] = datos['nombre'].strip()

        # Actualizar activo
        return self.repository.update(activo, **datos)

    def buscar_activos(self, query: str) -> list[Activo]:
        """
        Busca activos por código, nombre, número de serie o código de barras.

        Args:
            query: Término de búsqueda

        Returns:
            Lista de activos que coinciden con la búsqueda
        """
        return list(self.repository.search(query))

    def obtener_activos_por_categoria(self, categoria: CategoriaActivo) -> list[Activo]:
        """
        Obtiene todos los activos de una categoría.

        Args:
            categoria: Categoría a consultar

        Returns:
            Lista de activos de la categoría
        """
        return list(self.repository.filter_by_categoria(categoria))

    def obtener_activos_por_estado(self, estado: EstadoActivo) -> list[Activo]:
        """
        Obtiene todos los activos en un estado específico.

        Args:
            estado: Estado a consultar

        Returns:
            Lista de activos en ese estado
        """
        return list(self.repository.filter_by_estado(estado))


# ==================== MOVIMIENTO ACTIVO SERVICE ====================

class MovimientoActivoService:
    """
    Service para lógica de negocio de MovimientoActivo.

    Coordina operaciones complejas de movimientos siguiendo Clean Architecture.
    Todas las operaciones de movimiento son transacciones atómicas.
    """

    def __init__(self) -> None:
        self.movimiento_repo = MovimientoActivoRepository()

    @transaction.atomic
    def registrar_movimiento(
        self,
        activo: Activo,
        tipo_movimiento: TipoMovimientoActivo,
        usuario_registro: User,
        ubicacion_destino: Optional[Ubicacion] = None,
        taller: Optional[Taller] = None,
        responsable: Optional[User] = None,
        proveniencia: Optional[Proveniencia] = None,
        observaciones: Optional[str] = None
    ) -> MovimientoActivo:
        """
        Registra un movimiento de activo validando reglas de negocio.

        Esta operación es atómica (transaction.atomic): todo o nada.

        Args:
            activo: Activo a mover
            tipo_movimiento: Tipo de movimiento
            usuario_registro: Usuario que registra
            ubicacion_destino: Ubicación destino (opcional)
            taller: Taller (opcional)
            responsable: Responsable del activo (opcional)
            proveniencia: Proveniencia del activo (opcional)
            observaciones: Observaciones (opcional)

        Returns:
            Movimiento creado

        Raises:
            ValidationError: Si faltan datos requeridos o hay errores de validación
        """
        # Validar que el estado del activo permita movimiento
        if not activo.estado.permite_movimiento:
            raise ValidationError({
                'activo': f'El activo está en estado "{activo.estado.nombre}" '
                          f'que no permite movimientos.'
            })

        # Crear movimiento
        movimiento = self.movimiento_repo.create(
            activo=activo,
            tipo_movimiento=tipo_movimiento,
            usuario_registro=usuario_registro,
            ubicacion_destino=ubicacion_destino,
            taller=taller,
            responsable=responsable,
            proveniencia=proveniencia,
            observaciones=observaciones
        )

        return movimiento

    def obtener_historial_activo(
        self,
        activo: Activo,
        limit: int = 20
    ) -> list[MovimientoActivo]:
        """
        Obtiene el historial de movimientos de un activo.

        Args:
            activo: Activo del cual obtener el historial
            limit: Número máximo de movimientos a retornar (default: 20)

        Returns:
            Lista de movimientos ordenados por fecha descendente
        """
        return list(self.movimiento_repo.filter_by_activo(activo, limit))

    def obtener_ubicacion_actual(self, activo: Activo) -> Optional[Tuple[Ubicacion, User]]:
        """
        Obtiene la ubicación y responsable actual de un activo basado en su último movimiento.

        Args:
            activo: Activo del cual obtener la ubicación

        Returns:
            Tupla (ubicacion, responsable) si existe movimiento, None en caso contrario
        """
        ultimo_movimiento = self.movimiento_repo.get_ultimo_por_activo(activo)
        if ultimo_movimiento:
            return (ultimo_movimiento.ubicacion_destino, ultimo_movimiento.responsable)
        return None

    def obtener_movimientos_por_ubicacion(self, ubicacion: Ubicacion) -> list[MovimientoActivo]:
        """
        Obtiene todos los movimientos hacia una ubicación específica.

        Args:
            ubicacion: Ubicación a consultar

        Returns:
            Lista de movimientos hacia esa ubicación
        """
        return list(self.movimiento_repo.filter_by_ubicacion(ubicacion))

    def obtener_movimientos_por_responsable(self, responsable: User) -> list[MovimientoActivo]:
        """
        Obtiene todos los movimientos de un responsable.

        Args:
            responsable: Usuario responsable

        Returns:
            Lista de movimientos del responsable
        """
        return list(self.movimiento_repo.filter_by_responsable(responsable))


# ==================== SERVICIOS DE CATÁLOGOS ====================

class CategoriaActivoService:
    """Service para lógica de negocio de CategoriaActivo."""

    def __init__(self) -> None:
        self.repository = CategoriaActivoRepository()
        self.activo_repo = ActivoRepository()

    def eliminar_categoria(self, categoria: CategoriaActivo) -> Tuple[bool, str]:
        """
        Elimina lógicamente una categoría validando reglas de negocio.

        Valida que no tenga activos asociados activos.

        Args:
            categoria: Categoría a eliminar

        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # Verificar si tiene activos activos
        activos_activos = self.activo_repo.filter_by_categoria(categoria).filter(
            activo=True
        )

        if activos_activos.exists():
            count = activos_activos.count()
            return (
                False,
                f'No se puede eliminar la categoría porque tiene {count} '
                f'activo(s) activo(s) asociado(s).'
            )

        # Soft delete
        categoria.eliminado = True
        categoria.activo = False
        categoria.save()

        return (True, f'Categoría "{categoria.nombre}" eliminada exitosamente.')


class EstadoActivoService:
    """Service para lógica de negocio de EstadoActivo."""

    def __init__(self) -> None:
        self.repository = EstadoActivoRepository()
        self.activo_repo = ActivoRepository()

    def eliminar_estado(self, estado: EstadoActivo) -> Tuple[bool, str]:
        """
        Elimina lógicamente un estado validando reglas de negocio.

        Args:
            estado: Estado a eliminar

        Returns:
            Tupla (éxito: bool, mensaje: str)
        """
        # No permitir eliminar estado inicial
        if estado.es_inicial:
            return (
                False,
                'No se puede eliminar el estado inicial del sistema.'
            )

        # Verificar si tiene activos asociados
        activos_con_estado = self.activo_repo.filter_by_estado(estado).filter(
            activo=True
        )

        if activos_con_estado.exists():
            count = activos_con_estado.count()
            return (
                False,
                f'No se puede eliminar el estado porque hay {count} '
                f'activo(s) en este estado.'
            )

        # Soft delete
        estado.eliminado = True
        estado.activo = False
        estado.save()

        return (True, f'Estado "{estado.nombre}" eliminado exitosamente.')
