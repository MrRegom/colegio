"""
Service Layer para el módulo de compras.

Contiene la lógica de negocio siguiendo el principio de
Single Responsibility (SOLID). Las operaciones críticas
usan transacciones atómicas para garantizar consistencia.
"""
from typing import Optional, Dict, Any
from decimal import Decimal
from datetime import date
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.utils import validar_rut, format_rut, generar_codigo_unico
from .models import (
    Proveedor, EstadoOrdenCompra, OrdenCompra,
    DetalleOrdenCompra, DetalleOrdenCompraArticulo,
    EstadoRecepcion, RecepcionArticulo, DetalleRecepcionArticulo,
    RecepcionActivo, DetalleRecepcionActivo
)
from .repositories import (
    ProveedorRepository, EstadoOrdenCompraRepository, OrdenCompraRepository,
    DetalleOrdenCompraRepository, DetalleOrdenCompraArticuloRepository,
    EstadoRecepcionRepository, RecepcionArticuloRepository,
    DetalleRecepcionArticuloRepository, RecepcionActivoRepository,
    DetalleRecepcionActivoRepository
)
from apps.bodega.models import Bodega, Articulo
from apps.bodega.repositories import ArticuloRepository, BodegaRepository
from apps.activos.models import Activo
from apps.activos.repositories import ActivoRepository


# ==================== PROVEEDOR SERVICE ====================

class ProveedorService:
    """Service para lógica de negocio de Proveedores."""

    def __init__(self):
        self.proveedor_repo = ProveedorRepository()

    @transaction.atomic
    def crear_proveedor(
        self,
        rut: str,
        razon_social: str,
        direccion: str,
        **kwargs: Any
    ) -> Proveedor:
        """
        Crea un nuevo proveedor con validaciones.

        Args:
            rut: RUT del proveedor
            razon_social: Razón social
            direccion: Dirección
            **kwargs: Campos opcionales

        Returns:
            Proveedor: Proveedor creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar RUT
        if not validar_rut(rut):
            raise ValidationError({'rut': 'RUT inválido'})

        # Verificar RUT único
        if self.proveedor_repo.exists_by_rut(rut):
            raise ValidationError({'rut': 'Ya existe un proveedor con este RUT'})

        # Formatear RUT
        rut_formateado = format_rut(rut)

        # Crear proveedor
        proveedor = Proveedor.objects.create(
            rut=rut_formateado,
            razon_social=razon_social.strip(),
            direccion=direccion.strip(),
            nombre_fantasia=kwargs.get('nombre_fantasia', ''),
            giro=kwargs.get('giro', ''),
            comuna=kwargs.get('comuna', ''),
            ciudad=kwargs.get('ciudad', ''),
            telefono=kwargs.get('telefono', ''),
            email=kwargs.get('email', ''),
            sitio_web=kwargs.get('sitio_web', ''),
            condicion_pago=kwargs.get('condicion_pago', 'Contado'),
            dias_credito=kwargs.get('dias_credito', 0),
            activo=True
        )

        return proveedor

    @transaction.atomic
    def actualizar_proveedor(
        self,
        proveedor: Proveedor,
        **campos: Any
    ) -> Proveedor:
        """
        Actualiza un proveedor existente.

        Args:
            proveedor: Proveedor a actualizar
            **campos: Campos a actualizar

        Returns:
            Proveedor: Proveedor actualizado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Si se actualiza el RUT, validar
        if 'rut' in campos:
            nuevo_rut = campos['rut']
            if not validar_rut(nuevo_rut):
                raise ValidationError({'rut': 'RUT inválido'})

            # Verificar que no exista otro con ese RUT
            if self.proveedor_repo.exists_by_rut(nuevo_rut, exclude_id=proveedor.id):
                raise ValidationError({'rut': 'Ya existe otro proveedor con este RUT'})

            campos['rut'] = format_rut(nuevo_rut)

        # Actualizar campos
        for campo, valor in campos.items():
            setattr(proveedor, campo, valor)

        proveedor.save()
        return proveedor

    @transaction.atomic
    def eliminar_proveedor(self, proveedor: Proveedor) -> None:
        """
        Elimina (soft delete) un proveedor.

        Args:
            proveedor: Proveedor a eliminar

        Raises:
            ValidationError: Si el proveedor tiene órdenes asociadas
        """
        # Verificar que no tenga órdenes de compra
        orden_repo = OrdenCompraRepository()
        ordenes = orden_repo.filter_by_proveedor(proveedor)

        if ordenes.exists():
            raise ValidationError(
                'No se puede eliminar el proveedor porque tiene órdenes de compra asociadas'
            )

        # Soft delete
        proveedor.eliminado = True
        proveedor.activo = False
        proveedor.save()


# ==================== ORDEN COMPRA SERVICE ====================

class OrdenCompraService:
    """Service para lógica de negocio de Órdenes de Compra."""

    def __init__(self):
        self.orden_repo = OrdenCompraRepository()
        self.estado_repo = EstadoOrdenCompraRepository()
        self.proveedor_repo = ProveedorRepository()
        self.bodega_repo = BodegaRepository()

    def calcular_totales(
        self,
        subtotal: Decimal,
        tasa_impuesto: Decimal = Decimal('0.19'),  # 19% IVA Chile
        descuento: Decimal = Decimal('0')
    ) -> Dict[str, Decimal]:
        """
        Calcula los totales de una orden de compra.

        Args:
            subtotal: Subtotal sin impuestos
            tasa_impuesto: Tasa de impuesto (default: 19%)
            descuento: Descuento aplicado

        Returns:
            Dict con 'subtotal', 'impuesto', 'descuento', 'total'
        """
        impuesto = (subtotal - descuento) * tasa_impuesto
        total = subtotal - descuento + impuesto

        return {
            'subtotal': subtotal,
            'impuesto': impuesto,
            'descuento': descuento,
            'total': total
        }

    @transaction.atomic
    def crear_orden_compra(
        self,
        proveedor: Proveedor,
        bodega_destino: Bodega,
        solicitante: User,
        fecha_orden: date,
        numero: Optional[str] = None,
        **kwargs: Any
    ) -> OrdenCompra:
        """
        Crea una nueva orden de compra.

        Args:
            proveedor: Proveedor
            bodega_destino: Bodega de destino
            solicitante: Usuario solicitante
            fecha_orden: Fecha de la orden
            numero: Número de orden (opcional, se genera automático)
            **kwargs: Campos opcionales

        Returns:
            OrdenCompra: Orden creada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar proveedor activo
        if not proveedor.activo:
            raise ValidationError({'proveedor': 'El proveedor no está activo'})

        # Generar número si no se proporciona
        if not numero:
            numero = generar_codigo_unico('OC', OrdenCompra, 'numero', longitud=8)
        else:
            # Verificar que el número no exista
            if self.orden_repo.exists_by_numero(numero):
                raise ValidationError({'numero': 'Ya existe una orden con este número'})

        # Obtener estado inicial
        estado_inicial = self.estado_repo.get_inicial()
        if not estado_inicial:
            raise ValidationError('No se ha configurado un estado inicial para órdenes de compra')

        # Crear orden
        orden = OrdenCompra.objects.create(
            numero=numero,
            fecha_orden=fecha_orden,
            proveedor=proveedor,
            bodega_destino=bodega_destino,
            estado=estado_inicial,
            solicitante=solicitante,
            aprobador=kwargs.get('aprobador'),
            fecha_entrega_esperada=kwargs.get('fecha_entrega_esperada'),
            subtotal=Decimal('0'),
            impuesto=Decimal('0'),
            descuento=kwargs.get('descuento', Decimal('0')),
            total=Decimal('0'),
            observaciones=kwargs.get('observaciones', ''),
            notas_internas=kwargs.get('notas_internas', '')
        )

        return orden

    @transaction.atomic
    def cambiar_estado(
        self,
        orden: OrdenCompra,
        nuevo_estado: EstadoOrdenCompra,
        usuario: User
    ) -> OrdenCompra:
        """
        Cambia el estado de una orden de compra.

        Args:
            orden: Orden a actualizar
            nuevo_estado: Nuevo estado
            usuario: Usuario que realiza el cambio

        Returns:
            OrdenCompra: Orden actualizada

        Raises:
            ValidationError: Si el cambio no es válido
        """
        # Validar que el estado actual permita edición
        # Estados finales: RECIBIDA, CANCELADA, CERRADA
        estados_finales = ['RECIBIDA', 'CANCELADA', 'CERRADA']
        if orden.estado.codigo in estados_finales:
            raise ValidationError(f'No se puede cambiar el estado de una orden en estado {orden.estado.nombre}')

        # Actualizar estado
        orden.estado = nuevo_estado
        orden.save()

        return orden

    @transaction.atomic
    def recalcular_totales(self, orden: OrdenCompra) -> OrdenCompra:
        """
        Recalcula los totales de una orden basándose en sus detalles.

        Args:
            orden: Orden de compra

        Returns:
            OrdenCompra: Orden actualizada
        """
        # Sumar subtotales de detalles de activos
        detalle_repo = DetalleOrdenCompraRepository()
        detalles_activos = detalle_repo.filter_by_orden(orden)
        subtotal_activos = sum(d.subtotal for d in detalles_activos)

        # Sumar subtotales de detalles de artículos
        detalle_articulo_repo = DetalleOrdenCompraArticuloRepository()
        detalles_articulos = detalle_articulo_repo.filter_by_orden(orden)
        subtotal_articulos = sum(d.subtotal for d in detalles_articulos)

        # Subtotal total
        subtotal_total = subtotal_activos + subtotal_articulos

        # Calcular totales
        totales = self.calcular_totales(subtotal_total, descuento=orden.descuento)

        # Actualizar orden
        orden.subtotal = totales['subtotal']
        orden.impuesto = totales['impuesto']
        orden.total = totales['total']
        orden.save()

        return orden


# ==================== RECEPCIÓN SERVICE BASE (DRY) ====================

class RecepcionServiceBase:
    """
    Clase base abstracta para servicios de recepción.

    Implementa el patrón Template Method para reutilizar lógica común
    entre RecepcionArticuloService y RecepcionActivoService.
    """

    # Clases a sobrescribir por subclases
    model_class = None
    detalle_model_class = None
    repository_class = None
    detalle_repository_class = None
    item_repository_class = None

    def __init__(self):
        if not self.repository_class or not self.detalle_repository_class:
            raise NotImplementedError("Subclases deben definir repository_class y detalle_repository_class")

        self.recepcion_repo = self.repository_class()
        self.detalle_repo = self.detalle_repository_class()
        self.estado_repo = EstadoRecepcionRepository()
        self.item_repo = self.item_repository_class() if self.item_repository_class else None

    def _get_prefijo_numero(self) -> str:
        """Retorna el prefijo para generar el número de recepción."""
        raise NotImplementedError("Subclases deben implementar _get_prefijo_numero()")

    def _requiere_bodega(self) -> bool:
        """Indica si este tipo de recepción requiere bodega."""
        return False

    def _get_campos_especificos_recepcion(self, **kwargs) -> Dict[str, Any]:
        """
        Retorna campos específicos del modelo de recepción.

        Returns:
            Dict con campos adicionales específicos del tipo de recepción
        """
        return {}

    def _validar_campos_especificos(self, **kwargs) -> None:
        """
        Valida campos específicos antes de crear la recepción.

        Raises:
            ValidationError: Si hay errores de validación
        """
        pass

    @transaction.atomic
    def crear_recepcion(
        self,
        recibido_por: User,
        orden_compra: Optional[OrdenCompra] = None,
        numero: Optional[str] = None,
        **kwargs: Any
    ):
        """
        Crea una nueva recepción (Template Method).

        Args:
            recibido_por: Usuario que recibe
            orden_compra: Orden de compra asociada (opcional)
            numero: Número de recepción (opcional, se genera automático)
            **kwargs: Campos opcionales (bodega para artículos, etc.)

        Returns:
            Recepción creada (RecepcionArticulo o RecepcionActivo)

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar campos específicos
        self._validar_campos_especificos(**kwargs)

        # Generar número si no se proporciona
        if not numero:
            prefijo = self._get_prefijo_numero()
            numero = generar_codigo_unico(prefijo, self.model_class, 'numero', longitud=8)
        else:
            if self.recepcion_repo.exists_by_numero(numero):
                raise ValidationError({'numero': 'Ya existe una recepción con este número'})

        # Obtener estado inicial
        estado_inicial = self.estado_repo.get_inicial()
        if not estado_inicial:
            raise ValidationError('No se ha configurado un estado inicial para recepciones')

        # Preparar campos comunes
        campos_comunes = {
            'numero': numero,
            'orden_compra': orden_compra,
            'estado': estado_inicial,
            'recibido_por': recibido_por,
            'documento_referencia': kwargs.get('documento_referencia', ''),
            'observaciones': kwargs.get('observaciones', '')
        }

        # Agregar campos específicos de la subclase
        campos_especificos = self._get_campos_especificos_recepcion(**kwargs)
        campos_comunes.update(campos_especificos)

        # Crear recepción
        recepcion = self.model_class.objects.create(**campos_comunes)

        return recepcion

    @transaction.atomic
    def agregar_detalle(
        self,
        recepcion,
        item,
        cantidad: Decimal,
        **kwargs: Any
    ):
        """
        Agrega un detalle a la recepción (Template Method).

        Args:
            recepcion: Recepción
            item: Item recibido (Articulo o Activo)
            cantidad: Cantidad recibida
            **kwargs: Campos opcionales específicos

        Returns:
            Detalle creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar cantidad
        if cantidad <= 0:
            raise ValidationError({'cantidad': 'La cantidad debe ser mayor a cero'})

        # Validar que la recepción no esté finalizada
        # Estados finales: COMPLETADA, CANCELADA
        estados_finales_recepcion = ['COMPLETADA', 'CANCELADA', 'CERRADA']
        if recepcion.estado.codigo in estados_finales_recepcion:
            raise ValidationError(f'No se pueden agregar detalles a una recepción en estado {recepcion.estado.nombre}')

        # Validaciones específicas antes de crear detalle
        self._validar_antes_crear_detalle(recepcion, item, cantidad, **kwargs)

        # Crear detalle
        detalle = self._crear_detalle_interno(recepcion, item, cantidad, **kwargs)

        # Actualizar stock si aplica (solo para artículos)
        self._post_crear_detalle(recepcion, item, cantidad, **kwargs)

        # Si hay orden de compra, actualizar cantidad recibida
        if recepcion.orden_compra:
            self._actualizar_cantidad_recibida_orden(recepcion.orden_compra, item, cantidad)

        return detalle

    def _validar_antes_crear_detalle(self, recepcion, item, cantidad: Decimal, **kwargs) -> None:
        """
        Hook method para validaciones específicas antes de crear detalle.

        Args:
            recepcion: Recepción
            item: Item a recibir
            cantidad: Cantidad
            **kwargs: Campos adicionales

        Raises:
            ValidationError: Si hay errores de validación
        """
        pass

    def _crear_detalle_interno(self, recepcion, item, cantidad: Decimal, **kwargs):
        """
        Crea el detalle de recepción con campos específicos.

        Args:
            recepcion: Recepción
            item: Item recibido
            cantidad: Cantidad
            **kwargs: Campos específicos

        Returns:
            Detalle creado
        """
        raise NotImplementedError("Subclases deben implementar _crear_detalle_interno()")

    def _post_crear_detalle(self, recepcion, item, cantidad: Decimal, **kwargs) -> None:
        """
        Hook method para acciones después de crear el detalle.

        Por ejemplo, actualizar stock para artículos.

        Args:
            recepcion: Recepción
            item: Item recibido
            cantidad: Cantidad
            **kwargs: Campos adicionales
        """
        pass

    def _actualizar_cantidad_recibida_orden(
        self,
        orden: OrdenCompra,
        item,
        cantidad_adicional: Decimal
    ) -> None:
        """
        Actualiza la cantidad recibida en el detalle de la orden de compra.

        Método genérico que funciona para artículos y activos.

        Args:
            orden: Orden de compra
            item: Item recibido (Articulo o Activo)
            cantidad_adicional: Cantidad adicional recibida
        """
        # Determinar qué repositorio usar basándose en el tipo de item
        if hasattr(item, 'stock_actual'):  # Es un Artículo
            from apps.compras.repositories import DetalleOrdenCompraArticuloRepository
            detalle_orden_repo = DetalleOrdenCompraArticuloRepository()
            detalles = detalle_orden_repo.filter_by_orden(orden)
            campo_item = 'articulo'
        else:  # Es un Activo
            from apps.compras.repositories import DetalleOrdenCompraRepository
            detalle_orden_repo = DetalleOrdenCompraRepository()
            detalles = detalle_orden_repo.filter_by_orden(orden)
            campo_item = 'activo'

        # Buscar el detalle del item
        for detalle in detalles:
            if getattr(detalle, campo_item).id == item.id:
                detalle.cantidad_recibida += cantidad_adicional
                detalle.save()
                break


# ==================== RECEPCIÓN ARTÍCULO SERVICE ====================

class RecepcionArticuloService(RecepcionServiceBase):
    """Service para lógica de negocio de Recepciones de Artículos."""

    # Configuración de modelos y repositorios
    model_class = RecepcionArticulo
    detalle_model_class = DetalleRecepcionArticulo
    repository_class = RecepcionArticuloRepository
    detalle_repository_class = DetalleRecepcionArticuloRepository
    item_repository_class = ArticuloRepository

    def _get_prefijo_numero(self) -> str:
        """Retorna el prefijo para el número de recepción de artículos."""
        return 'RART'

    def _requiere_bodega(self) -> bool:
        """Los artículos requieren bodega."""
        return True

    def _validar_campos_especificos(self, **kwargs) -> None:
        """
        Valida que se proporcione bodega para artículos.

        Raises:
            ValidationError: Si no se proporciona bodega
        """
        if 'bodega' not in kwargs or kwargs['bodega'] is None:
            raise ValidationError({'bodega': 'Debe especificar una bodega para recepción de artículos'})

    def _get_campos_especificos_recepcion(self, **kwargs) -> Dict[str, Any]:
        """
        Retorna campos específicos para recepción de artículos.

        Returns:
            Dict con campo 'bodega'
        """
        return {
            'bodega': kwargs.get('bodega')
        }

    def _crear_detalle_interno(
        self,
        recepcion: RecepcionArticulo,
        item: Articulo,
        cantidad: Decimal,
        **kwargs
    ) -> DetalleRecepcionArticulo:
        """
        Crea el detalle de recepción de artículo.

        Args:
            recepcion: Recepción
            item: Artículo
            cantidad: Cantidad
            **kwargs: lote, fecha_vencimiento, observaciones

        Returns:
            DetalleRecepcionArticulo creado
        """
        return DetalleRecepcionArticulo.objects.create(
            recepcion=recepcion,
            articulo=item,
            cantidad=cantidad,
            lote=kwargs.get('lote', ''),
            fecha_vencimiento=kwargs.get('fecha_vencimiento'),
            observaciones=kwargs.get('observaciones', '')
        )

    def _post_crear_detalle(
        self,
        recepcion: RecepcionArticulo,
        item: Articulo,
        cantidad: Decimal,
        **kwargs
    ) -> None:
        """
        Actualiza el stock del artículo después de crear el detalle.

        Args:
            recepcion: Recepción
            item: Artículo
            cantidad: Cantidad recibida
            **kwargs: actualizar_stock (default: True)

        Raises:
            ValidationError: Si excede stock máximo
        """
        actualizar_stock = kwargs.get('actualizar_stock', True)

        if actualizar_stock:
            stock_nuevo = item.stock_actual + cantidad

            # Validar stock máximo
            if item.stock_maximo and stock_nuevo > item.stock_maximo:
                raise ValidationError(
                    f'La cantidad recibida excede el stock máximo del artículo '
                    f'({item.stock_maximo})'
                )

            item.stock_actual = stock_nuevo
            item.save()

    # Método compatible con código existente que espera parámetro 'bodega'
    @transaction.atomic
    def crear_recepcion(
        self,
        recibido_por: User,
        bodega: Optional[Bodega] = None,
        orden_compra: Optional[OrdenCompra] = None,
        numero: Optional[str] = None,
        **kwargs: Any
    ) -> RecepcionArticulo:
        """
        Crea una nueva recepción de artículos.

        Args:
            recibido_por: Usuario que recibe
            bodega: Bodega de recepción (requerido)
            orden_compra: Orden de compra asociada (opcional)
            numero: Número de recepción (opcional, se genera automático)
            **kwargs: Campos opcionales

        Returns:
            RecepcionArticulo: Recepción creada

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Agregar bodega a kwargs para que la clase base la procese
        kwargs['bodega'] = bodega
        return super().crear_recepcion(
            recibido_por=recibido_por,
            orden_compra=orden_compra,
            numero=numero,
            **kwargs
        )

    # Método compatible con código existente
    @transaction.atomic
    def agregar_detalle(
        self,
        recepcion: RecepcionArticulo,
        articulo: Articulo,
        cantidad: Decimal,
        actualizar_stock: bool = True,
        **kwargs: Any
    ) -> DetalleRecepcionArticulo:
        """
        Agrega un detalle a la recepción y actualiza el stock.

        Args:
            recepcion: Recepción
            articulo: Artículo recibido
            cantidad: Cantidad recibida
            actualizar_stock: Si debe actualizar el stock (default: True)
            **kwargs: Campos opcionales (lote, fecha_vencimiento, observaciones)

        Returns:
            DetalleRecepcionArticulo: Detalle creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        kwargs['actualizar_stock'] = actualizar_stock
        return super().agregar_detalle(recepcion, articulo, cantidad, **kwargs)


# ==================== RECEPCIÓN ACTIVO SERVICE ====================

class RecepcionActivoService(RecepcionServiceBase):
    """Service para lógica de negocio de Recepciones de Activos."""

    # Configuración de modelos y repositorios
    model_class = RecepcionActivo
    detalle_model_class = DetalleRecepcionActivo
    repository_class = RecepcionActivoRepository
    detalle_repository_class = DetalleRecepcionActivoRepository
    item_repository_class = ActivoRepository

    def _get_prefijo_numero(self) -> str:
        """Retorna el prefijo para el número de recepción de activos."""
        return 'RACT'

    def _requiere_bodega(self) -> bool:
        """Los activos NO requieren bodega."""
        return False

    def _validar_antes_crear_detalle(
        self,
        recepcion: RecepcionActivo,
        item: Activo,
        cantidad: Decimal,
        **kwargs
    ) -> None:
        """
        Valida que el activo tenga número de serie si lo requiere.

        Args:
            recepcion: Recepción
            item: Activo
            cantidad: Cantidad
            **kwargs: numero_serie

        Raises:
            ValidationError: Si el activo requiere serie y no se proporciona
        """
        numero_serie = kwargs.get('numero_serie')
        if item.requiere_serie and not numero_serie:
            raise ValidationError(
                {'numero_serie': 'Este activo requiere número de serie'}
            )

    def _crear_detalle_interno(
        self,
        recepcion: RecepcionActivo,
        item: Activo,
        cantidad: Decimal,
        **kwargs
    ) -> DetalleRecepcionActivo:
        """
        Crea el detalle de recepción de activo.

        Args:
            recepcion: Recepción
            item: Activo
            cantidad: Cantidad
            **kwargs: numero_serie, observaciones

        Returns:
            DetalleRecepcionActivo creado
        """
        numero_serie = kwargs.get('numero_serie', '')
        return DetalleRecepcionActivo.objects.create(
            recepcion=recepcion,
            activo=item,
            cantidad=cantidad,
            numero_serie=numero_serie,
            observaciones=kwargs.get('observaciones', '')
        )

    # Los activos NO actualizan stock, por lo que _post_crear_detalle
    # usa la implementación vacía de la clase base

    # Métodos compatibles con código existente
    @transaction.atomic
    def agregar_detalle(
        self,
        recepcion: RecepcionActivo,
        activo: Activo,
        cantidad: Decimal,
        **kwargs: Any
    ) -> DetalleRecepcionActivo:
        """
        Agrega un detalle a la recepción de activos.

        Args:
            recepcion: Recepción
            activo: Activo recibido
            cantidad: Cantidad recibida
            **kwargs: Campos opcionales (numero_serie, observaciones)

        Returns:
            DetalleRecepcionActivo: Detalle creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        return super().agregar_detalle(recepcion, activo, cantidad, **kwargs)
