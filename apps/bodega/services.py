"""
Service Layer para el módulo de bodega.

Contiene la lógica de negocio y coordina los repositories,
siguiendo el principio de Single Responsibility (SOLID).
"""
from typing import Optional, Dict, Any, Tuple
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import (
    Categoria, Articulo, TipoMovimiento, Movimiento, Bodega,
    EstadoEntrega, TipoEntrega, EntregaArticulo, DetalleEntregaArticulo,
    EntregaBien, DetalleEntregaBien
)
from .repositories import (
    CategoriaRepository,
    ArticuloRepository,
    TipoMovimientoRepository,
    MovimientoRepository,
    BodegaRepository,
    EstadoEntregaRepository,
    TipoEntregaRepository,
    EntregaArticuloRepository,
    DetalleEntregaArticuloRepository,
    EntregaBienRepository,
    DetalleEntregaBienRepository
)


# ==================== CATEGORÍA SERVICE ====================

class CategoriaService:
    """
    Service para lógica de negocio de Categoría.

    Coordina operaciones complejas y validaciones de negocio.
    """

    def __init__(self):
        self.repository = CategoriaRepository()

    def crear_categoria(
        self,
        codigo: str,
        nombre: str,
        descripcion: Optional[str] = None,
        observaciones: Optional[str] = None
    ) -> Categoria:
        """
        Crea una nueva categoría validando que no exista el código.

        Args:
            codigo: Código único de la categoría
            nombre: Nombre de la categoría
            descripcion: Descripción opcional
            observaciones: Observaciones opcionales

        Returns:
            Categoría creada

        Raises:
            ValidationError: Si el código ya existe
        """
        # Validar unicidad del código
        if self.repository.exists_by_codigo(codigo):
            raise ValidationError(
                f'Ya existe una categoría con el código "{codigo}".'
            )

        # Crear categoría
        categoria = Categoria.objects.create(
            codigo=codigo.strip().upper(),
            nombre=nombre.strip(),
            descripcion=descripcion,
            observaciones=observaciones
        )

        return categoria

    def actualizar_categoria(
        self,
        categoria: Categoria,
        codigo: Optional[str] = None,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        observaciones: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> Categoria:
        """
        Actualiza una categoría existente.

        Args:
            categoria: Categoría a actualizar
            codigo: Nuevo código (opcional)
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
            observaciones: Nuevas observaciones (opcional)
            activo: Nuevo estado activo (opcional)

        Returns:
            Categoría actualizada

        Raises:
            ValidationError: Si el nuevo código ya existe
        """
        # Validar código si se está actualizando
        if codigo and codigo != categoria.codigo:
            if self.repository.exists_by_codigo(codigo, exclude_id=categoria.id):
                raise ValidationError(
                    f'Ya existe una categoría con el código "{codigo}".'
                )
            categoria.codigo = codigo.strip().upper()

        # Actualizar campos
        if nombre:
            categoria.nombre = nombre.strip()
        if descripcion is not None:
            categoria.descripcion = descripcion
        if observaciones is not None:
            categoria.observaciones = observaciones
        if activo is not None:
            categoria.activo = activo

        categoria.save()
        return categoria

    def eliminar_categoria(self, categoria: Categoria) -> Tuple[bool, str]:
        """
        Elimina lógicamente una categoría (soft delete).

        Valida que no tenga artículos asociados activos.

        Args:
            categoria: Categoría a eliminar

        Returns:
            Tupla (éxito, mensaje)
        """
        # Verificar si tiene artículos activos
        articulos_activos = ArticuloRepository.filter_by_categoria(categoria).filter(
            activo=True
        )

        if articulos_activos.exists():
            count = articulos_activos.count()
            return (
                False,
                f'No se puede eliminar la categoría porque tiene {count} '
                f'artículo(s) activo(s) asociado(s).'
            )

        # Soft delete
        categoria.eliminado = True
        categoria.activo = False
        categoria.save()

        return (True, f'Categoría "{categoria.nombre}" eliminada exitosamente.')


# ==================== ARTÍCULO SERVICE ====================

class ArticuloService:
    """
    Service para lógica de negocio de Artículo.

    Coordina operaciones complejas y validaciones de negocio.
    """

    def __init__(self):
        self.repository = ArticuloRepository()

    def crear_articulo(
        self,
        codigo: str,
        nombre: str,
        categoria: Categoria,
        ubicacion_fisica: Bodega,
        unidad_medida: str,
        stock_minimo: Decimal = Decimal('0'),
        stock_maximo: Optional[Decimal] = None,
        punto_reorden: Optional[Decimal] = None,
        descripcion: Optional[str] = None,
        marca: Optional[str] = None,
        observaciones: Optional[str] = None
    ) -> Articulo:
        """
        Crea un nuevo artículo validando que no exista el código.

        Args:
            codigo: Código único del artículo
            nombre: Nombre del artículo
            categoria: Categoría del artículo
            ubicacion_fisica: Bodega donde se almacena
            unidad_medida: Unidad de medida
            stock_minimo: Stock mínimo permitido
            stock_maximo: Stock máximo permitido (opcional)
            punto_reorden: Punto de reorden (opcional)
            descripcion: Descripción (opcional)
            marca: Marca (opcional)
            observaciones: Observaciones (opcional)

        Returns:
            Artículo creado

        Raises:
            ValidationError: Si el código ya existe o hay errores de validación
        """
        # Validar unicidad del código
        if self.repository.exists_by_codigo(codigo):
            raise ValidationError(
                f'Ya existe un artículo con el código "{codigo}".'
            )

        # Validar stock_maximo > stock_minimo
        if stock_maximo and stock_maximo < stock_minimo:
            raise ValidationError(
                'El stock máximo no puede ser menor que el stock mínimo.'
            )

        # Validar punto_reorden >= stock_minimo
        if punto_reorden and punto_reorden < stock_minimo:
            raise ValidationError(
                'El punto de reorden no puede ser menor que el stock mínimo.'
            )

        # Crear artículo
        articulo = Articulo.objects.create(
            codigo=codigo.strip().upper(),
            nombre=nombre.strip(),
            categoria=categoria,
            ubicacion_fisica=ubicacion_fisica,
            unidad_medida=unidad_medida.strip(),
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            punto_reorden=punto_reorden,
            descripcion=descripcion,
            marca=marca,
            observaciones=observaciones
        )

        return articulo

    def actualizar_articulo(
        self,
        articulo: Articulo,
        datos: Dict[str, Any]
    ) -> Articulo:
        """
        Actualiza un artículo existente.

        Args:
            articulo: Artículo a actualizar
            datos: Diccionario con los datos a actualizar

        Returns:
            Artículo actualizado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar código si se está actualizando
        if 'codigo' in datos and datos['codigo'] != articulo.codigo:
            if self.repository.exists_by_codigo(datos['codigo'], exclude_id=articulo.id):
                raise ValidationError(
                    f'Ya existe un artículo con el código "{datos["codigo"]}".'
                )

        # Validar stocks
        stock_min = datos.get('stock_minimo', articulo.stock_minimo)
        stock_max = datos.get('stock_maximo', articulo.stock_maximo)
        punto_reorden = datos.get('punto_reorden', articulo.punto_reorden)

        if stock_max and stock_max < stock_min:
            raise ValidationError(
                'El stock máximo no puede ser menor que el stock mínimo.'
            )

        if punto_reorden and punto_reorden < stock_min:
            raise ValidationError(
                'El punto de reorden no puede ser menor que el stock mínimo.'
            )

        # Actualizar campos
        for campo, valor in datos.items():
            if hasattr(articulo, campo):
                if campo in ['codigo', 'nombre', 'unidad_medida'] and isinstance(valor, str):
                    valor = valor.strip().upper() if campo == 'codigo' else valor.strip()
                setattr(articulo, campo, valor)

        articulo.save()
        return articulo

    def obtener_articulos_bajo_stock(self) -> list[Articulo]:
        """
        Retorna lista de artículos con stock bajo el mínimo.

        Returns:
            Lista de artículos con stock crítico
        """
        return list(self.repository.get_low_stock())

    def obtener_articulos_punto_reorden(self) -> list[Articulo]:
        """
        Retorna lista de artículos que alcanzaron el punto de reorden.

        Returns:
            Lista de artículos que requieren reorden
        """
        return list(self.repository.get_reorder_point())


# ==================== MOVIMIENTO SERVICE ====================

class MovimientoService:
    """
    Service para lógica de negocio de Movimiento.

    Coordina operaciones complejas de movimientos de inventario
    con actualización atómica de stock.
    """

    def __init__(self):
        self.movimiento_repo = MovimientoRepository()
        self.articulo_repo = ArticuloRepository()
        self.tipo_repo = TipoMovimientoRepository()

    @transaction.atomic
    def registrar_entrada(
        self,
        articulo: Articulo,
        tipo: TipoMovimiento,
        cantidad: Decimal,
        usuario: User,
        motivo: str
    ) -> Movimiento:
        """
        Registra una entrada de inventario (aumenta stock).

        Esta operación es atómica: todo o nada.

        Args:
            articulo: Artículo a mover
            tipo: Tipo de movimiento
            cantidad: Cantidad a ingresar
            usuario: Usuario que realiza la operación
            motivo: Motivo del movimiento

        Returns:
            Movimiento creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar cantidad
        if cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a cero.')

        # Calcular nuevo stock
        stock_anterior = articulo.stock_actual
        stock_nuevo = stock_anterior + cantidad

        # Validar stock máximo si está definido
        if articulo.stock_maximo and stock_nuevo > articulo.stock_maximo:
            raise ValidationError(
                f'La cantidad excede el stock máximo permitido '
                f'({articulo.stock_maximo}). Stock actual: {stock_anterior}, '
                f'intentando agregar: {cantidad}.'
            )

        # Crear movimiento
        movimiento = self.movimiento_repo.create(
            articulo=articulo,
            tipo=tipo,
            cantidad=cantidad,
            operacion='ENTRADA',
            usuario=usuario,
            motivo=motivo,
            stock_antes=stock_anterior,
            stock_despues=stock_nuevo
        )

        # Actualizar stock del artículo
        self.articulo_repo.update_stock(articulo, stock_nuevo)

        return movimiento

    @transaction.atomic
    def registrar_salida(
        self,
        articulo: Articulo,
        tipo: TipoMovimiento,
        cantidad: Decimal,
        usuario: User,
        motivo: str
    ) -> Movimiento:
        """
        Registra una salida de inventario (disminuye stock).

        Esta operación es atómica: todo o nada.

        Args:
            articulo: Artículo a mover
            tipo: Tipo de movimiento
            cantidad: Cantidad a sacar
            usuario: Usuario que realiza la operación
            motivo: Motivo del movimiento

        Returns:
            Movimiento creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar cantidad
        if cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a cero.')

        # Calcular nuevo stock
        stock_anterior = articulo.stock_actual
        stock_nuevo = stock_anterior - cantidad

        # Validar que no quede en negativo
        if stock_nuevo < 0:
            raise ValidationError(
                f'Stock insuficiente. Stock actual: {stock_anterior}, '
                f'intentando sacar: {cantidad}.'
            )

        # Crear movimiento
        movimiento = self.movimiento_repo.create(
            articulo=articulo,
            tipo=tipo,
            cantidad=cantidad,
            operacion='SALIDA',
            usuario=usuario,
            motivo=motivo,
            stock_antes=stock_anterior,
            stock_despues=stock_nuevo
        )

        # Actualizar stock del artículo
        self.articulo_repo.update_stock(articulo, stock_nuevo)

        return movimiento

    @transaction.atomic
    def registrar_movimiento(
        self,
        articulo: Articulo,
        tipo: TipoMovimiento,
        cantidad: Decimal,
        operacion: str,
        usuario: User,
        motivo: str
    ) -> Movimiento:
        """
        Registra un movimiento (entrada o salida) según la operación.

        Esta operación es atómica: todo o nada.

        Args:
            articulo: Artículo a mover
            tipo: Tipo de movimiento
            cantidad: Cantidad a mover
            operacion: 'ENTRADA' o 'SALIDA'
            usuario: Usuario que realiza la operación
            motivo: Motivo del movimiento

        Returns:
            Movimiento creado

        Raises:
            ValidationError: Si hay errores de validación
        """
        if operacion == 'ENTRADA':
            return self.registrar_entrada(articulo, tipo, cantidad, usuario, motivo)
        elif operacion == 'SALIDA':
            return self.registrar_salida(articulo, tipo, cantidad, usuario, motivo)
        else:
            raise ValidationError(
                f'Operación inválida: "{operacion}". '
                f'Debe ser "ENTRADA" o "SALIDA".'
            )

    def obtener_historial_articulo(
        self,
        articulo: Articulo,
        limit: int = 20
    ) -> list[Movimiento]:
        """
        Obtiene el historial de movimientos de un artículo.

        Args:
            articulo: Artículo del cual obtener el historial
            limit: Número máximo de movimientos a retornar

        Returns:
            Lista de movimientos ordenados por fecha descendente
        """
        return list(self.movimiento_repo.filter_by_articulo(articulo, limit))


# ==================== ENTREGA SERVICE ====================

class EntregaArticuloService:
    """
    Service para lógica de negocio de EntregaArticulo.

    Coordina operaciones complejas de entregas de artículos
    con actualización atómica de stock y validaciones.
    """

    def __init__(self):
        self.entrega_repo = EntregaArticuloRepository()
        self.articulo_repo = ArticuloRepository()
        self.estado_repo = EstadoEntregaRepository()
        self.tipo_repo = TipoEntregaRepository()
        self.movimiento_repo = MovimientoRepository()

    def generar_numero_entrega(self) -> str:
        """
        Genera un número único para la entrega.

        Returns:
            Número de entrega en formato ENT-ART-YYYYMMDD-XXX
        """
        from django.utils import timezone
        fecha_actual = timezone.now()
        prefijo = f"ENT-ART-{fecha_actual.strftime('%Y%m%d')}"

        # Buscar el último número del día
        ultimas_entregas = EntregaArticulo.objects.filter(
            numero__startswith=prefijo
        ).order_by('-numero')[:1]

        if ultimas_entregas.exists():
            ultimo_numero = ultimas_entregas[0].numero
            secuencia = int(ultimo_numero.split('-')[-1]) + 1
        else:
            secuencia = 1

        return f"{prefijo}-{secuencia:03d}"

    @transaction.atomic
    def crear_entrega(
        self,
        bodega_origen: Bodega,
        tipo: TipoEntrega,
        entregado_por: User,
        recibido_por: User,
        motivo: str,
        detalles: list[Dict[str, Any]],
        departamento_destino = None,
        observaciones: Optional[str] = None,
        solicitud = None
    ) -> EntregaArticulo:
        """
        Crea una nueva entrega de artículos con sus detalles.

        Esta operación es atómica: todo o nada.

        Args:
            bodega_origen: Bodega de donde salen los artículos
            tipo: Tipo de entrega
            entregado_por: Usuario que entrega
            recibido_por: Usuario que recibe
            motivo: Motivo de la entrega
            detalles: Lista de dicts con 'articulo_id', 'cantidad', 'lote' (opcional),
                     'observaciones' (opcional), 'detalle_solicitud_id' (opcional)
            departamento_destino: Departamento destino (opcional)
            observaciones: Observaciones generales (opcional)
            solicitud: Solicitud asociada (opcional)

        Returns:
            EntregaArticulo creada con sus detalles

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que haya detalles
        if not detalles or len(detalles) == 0:
            raise ValidationError('Debe agregar al menos un artículo a la entrega.')

        # Obtener estado inicial
        estado = self.estado_repo.get_inicial()
        if not estado:
            raise ValidationError(
                'No se encontró un estado inicial para las entregas. '
                'Configure los estados en el sistema.'
            )

        # Generar número de entrega
        numero = self.generar_numero_entrega()

        # Crear entrega
        entrega = EntregaArticulo.objects.create(
            numero=numero,
            bodega_origen=bodega_origen,
            tipo=tipo,
            estado=estado,
            entregado_por=entregado_por,
            recibido_por=recibido_por,
            departamento_destino=departamento_destino,
            motivo=motivo,
            observaciones=observaciones,
            solicitud=solicitud
        )

        # Procesar detalles y actualizar stock
        for detalle_data in detalles:
            articulo_id = detalle_data.get('articulo_id')
            cantidad = Decimal(str(detalle_data.get('cantidad', 0)))
            lote = detalle_data.get('lote')
            obs_detalle = detalle_data.get('observaciones')
            detalle_solicitud_id = detalle_data.get('detalle_solicitud_id')

            # Obtener artículo
            articulo = self.articulo_repo.get_by_id(articulo_id)
            if not articulo:
                raise ValidationError(f'No se encontró el artículo con ID {articulo_id}.')

            # Si hay detalle de solicitud, validar cantidad pendiente
            detalle_solicitud = None
            if detalle_solicitud_id:
                from apps.solicitudes.models import DetalleSolicitud
                try:
                    detalle_solicitud = DetalleSolicitud.objects.get(
                        id=detalle_solicitud_id,
                        eliminado=False
                    )

                    # Validar que la cantidad no exceda la pendiente
                    cantidad_pendiente = detalle_solicitud.cantidad_aprobada - detalle_solicitud.cantidad_despachada
                    if cantidad > cantidad_pendiente:
                        raise ValidationError(
                            f'La cantidad a entregar ({cantidad}) excede la cantidad pendiente '
                            f'({cantidad_pendiente}) del artículo {articulo.codigo} en la solicitud.'
                        )
                except DetalleSolicitud.DoesNotExist:
                    raise ValidationError(
                        f'No se encontró el detalle de solicitud con ID {detalle_solicitud_id}.'
                    )

            # Validar stock disponible
            if articulo.stock_actual < cantidad:
                raise ValidationError(
                    f'Stock insuficiente del artículo {articulo.codigo}. '
                    f'Disponible: {articulo.stock_actual}, Solicitado: {cantidad}'
                )

            # Crear detalle de entrega
            DetalleEntregaArticulo.objects.create(
                entrega=entrega,
                articulo=articulo,
                cantidad=cantidad,
                lote=lote,
                observaciones=obs_detalle,
                detalle_solicitud=detalle_solicitud
            )

            # Actualizar stock (restar)
            stock_anterior = articulo.stock_actual
            stock_nuevo = stock_anterior - cantidad
            self.articulo_repo.update_stock(articulo, stock_nuevo)

            # Si hay detalle de solicitud, actualizar cantidad despachada
            if detalle_solicitud:
                detalle_solicitud.cantidad_despachada += cantidad
                detalle_solicitud.save()

            # Registrar movimiento de salida
            tipo_mov_entrega = TipoMovimiento.objects.filter(
                codigo='ENTREGA'
            ).first()

            if not tipo_mov_entrega:
                # Si no existe, usar un tipo genérico de salida
                tipo_mov_entrega = TipoMovimiento.objects.filter(
                    activo=True, eliminado=False
                ).first()

            if tipo_mov_entrega:
                self.movimiento_repo.create(
                    articulo=articulo,
                    tipo=tipo_mov_entrega,
                    cantidad=cantidad,
                    operacion='SALIDA',
                    usuario=entregado_por,
                    motivo=f'Entrega {numero} - {motivo}',
                    stock_antes=stock_anterior,
                    stock_despues=stock_nuevo
                )

        # Si hay solicitud asociada, verificar si está completamente despachada
        if solicitud:
            self._verificar_y_actualizar_estado_solicitud(solicitud)

        return entrega

    def _verificar_y_actualizar_estado_solicitud(self, solicitud):
        """
        Verifica si todos los artículos de una solicitud están completamente despachados
        y actualiza el estado si corresponde.

        Args:
            solicitud: Solicitud a verificar
        """
        from apps.solicitudes.models import EstadoSolicitud

        # Verificar si todos los detalles están completamente despachados
        detalles = solicitud.detalles.filter(eliminado=False)
        todos_despachados = all(
            detalle.cantidad_despachada >= detalle.cantidad_aprobada
            for detalle in detalles
            if detalle.articulo  # Solo artículos
        )

        if todos_despachados:
            # Buscar estado "Completado" o similar
            estado_completado = EstadoSolicitud.objects.filter(
                es_final=True,
                activo=True,
                eliminado=False
            ).first()

            if estado_completado:
                solicitud.estado = estado_completado
                solicitud.save()


class EntregaBienService:
    """
    Service para lógica de negocio de EntregaBien.

    Coordina operaciones complejas de entregas de bienes/activos.
    """

    def __init__(self):
        self.entrega_repo = EntregaBienRepository()
        self.estado_repo = EstadoEntregaRepository()
        self.tipo_repo = TipoEntregaRepository()

    def generar_numero_entrega(self) -> str:
        """
        Genera un número único para la entrega de bien.

        Returns:
            Número de entrega en formato ENT-BIEN-YYYYMMDD-XXX
        """
        from django.utils import timezone
        fecha_actual = timezone.now()
        prefijo = f"ENT-BIEN-{fecha_actual.strftime('%Y%m%d')}"

        # Buscar el último número del día
        ultimas_entregas = EntregaBien.objects.filter(
            numero__startswith=prefijo
        ).order_by('-numero')[:1]

        if ultimas_entregas.exists():
            ultimo_numero = ultimas_entregas[0].numero
            secuencia = int(ultimo_numero.split('-')[-1]) + 1
        else:
            secuencia = 1

        return f"{prefijo}-{secuencia:03d}"

    @transaction.atomic
    def crear_entrega(
        self,
        tipo: TipoEntrega,
        entregado_por: User,
        recibido_por: User,
        motivo: str,
        detalles: list[Dict[str, Any]],
        departamento_destino = None,
        observaciones: Optional[str] = None
    ) -> EntregaBien:
        """
        Crea una nueva entrega de bienes con sus detalles.

        Esta operación es atómica: todo o nada.

        Args:
            tipo: Tipo de entrega
            entregado_por: Usuario que entrega
            recibido_por: Usuario que recibe
            motivo: Motivo de la entrega
            detalles: Lista de dicts con 'equipo_id', 'cantidad', 'numero_serie' (opcional), 'estado_fisico' (opcional), 'observaciones' (opcional)
            departamento_destino: Departamento destino (opcional)
            observaciones: Observaciones generales (opcional)

        Returns:
            EntregaBien creada con sus detalles

        Raises:
            ValidationError: Si hay errores de validación
        """
        # Validar que haya detalles
        if not detalles or len(detalles) == 0:
            raise ValidationError('Debe agregar al menos un bien a la entrega.')

        # Obtener estado inicial
        estado = self.estado_repo.get_inicial()
        if not estado:
            raise ValidationError(
                'No se encontró un estado inicial para las entregas. '
                'Configure los estados en el sistema.'
            )

        # Generar número de entrega
        numero = self.generar_numero_entrega()

        # Crear entrega
        entrega = EntregaBien.objects.create(
            numero=numero,
            tipo=tipo,
            estado=estado,
            entregado_por=entregado_por,
            recibido_por=recibido_por,
            departamento_destino=departamento_destino,
            motivo=motivo,
            observaciones=observaciones
        )

        # Procesar detalles
        for detalle_data in detalles:
            equipo_id = detalle_data.get('equipo_id')
            cantidad = Decimal(str(detalle_data.get('cantidad', 0)))
            numero_serie = detalle_data.get('numero_serie')
            estado_fisico = detalle_data.get('estado_fisico')
            obs_detalle = detalle_data.get('observaciones')

            # Obtener activo - necesitamos importar el modelo
            from apps.activos.models import Activo
            try:
                activo = Activo.objects.get(id=equipo_id, eliminado=False)
            except Activo.DoesNotExist:
                raise ValidationError(f'No se encontró el activo/bien con ID {equipo_id}.')

            # Crear detalle de entrega
            DetalleEntregaBien.objects.create(
                entrega=entrega,
                activo=activo,
                cantidad=cantidad,
                numero_serie=numero_serie,
                estado_fisico=estado_fisico,
                observaciones=obs_detalle
            )

        return entrega
