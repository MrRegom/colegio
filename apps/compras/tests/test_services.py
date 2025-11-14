"""
Tests para la capa de servicios del módulo de compras.

Siguiendo TDD y el patrón Arrange-Act-Assert.
Cobertura de funcionalidades críticas de negocio.
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.compras.services import (
    ProveedorService,
    OrdenCompraService,
    RecepcionArticuloService,
    RecepcionActivoService
)
from apps.compras.models import Proveedor, OrdenCompra
from apps.compras.tests.factories import (
    ProveedorFactory, OrdenCompraFactory, BodegaFactory,
    EstadoOrdenCompraFactory, EstadoRecepcionFactory,
    ArticuloFactory, ActivoFactory, UserFactory,
    TipoRecepcionFactory, RecepcionArticuloFactory,
    RecepcionActivoFactory
)


# ==================== TESTS DE PROVEEDOR SERVICE ====================

@pytest.mark.django_db
class TestProveedorService:
    """Tests para ProveedorService."""

    def test_crear_proveedor_valido_crea_exitosamente(self):
        """
        GIVEN: Datos válidos de un proveedor
        WHEN: Se llama a crear_proveedor
        THEN: Se crea el proveedor correctamente
        """
        # Arrange
        service = ProveedorService()

        # Act
        proveedor = service.crear_proveedor(
            rut='11111111-1',
            razon_social='Test S.A.',
            direccion='Calle Test 123',
            email='test@example.com'
        )

        # Assert
        assert proveedor.id is not None
        assert proveedor.rut == '11.111.111-1'  # RUT formateado
        assert proveedor.razon_social == 'Test S.A.'
        assert proveedor.activo is True

    def test_crear_proveedor_rut_invalido_lanza_excepcion(self):
        """
        GIVEN: Un RUT inválido
        WHEN: Se intenta crear un proveedor
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = ProveedorService()

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.crear_proveedor(
                rut='12345678-0',  # RUT inválido
                razon_social='Test S.A.',
                direccion='Calle Test 123'
            )

        assert 'rut' in exc_info.value.message_dict

    def test_crear_proveedor_rut_duplicado_lanza_excepcion(self):
        """
        GIVEN: Un proveedor existente con un RUT
        WHEN: Se intenta crear otro proveedor con el mismo RUT
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = ProveedorService()
        proveedor_existente = ProveedorFactory(rut='76.123.456-7')

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.crear_proveedor(
                rut='76123456-7',
                razon_social='Otro Proveedor',
                direccion='Otra Calle 456'
            )

        assert 'rut' in exc_info.value.message_dict

    def test_actualizar_proveedor_campos_actualiza_correctamente(self):
        """
        GIVEN: Un proveedor existente
        WHEN: Se actualizan sus campos
        THEN: Los cambios se persisten correctamente
        """
        # Arrange
        service = ProveedorService()
        proveedor = ProveedorFactory(razon_social='Nombre Original')

        # Act
        proveedor_actualizado = service.actualizar_proveedor(
            proveedor,
            razon_social='Nombre Actualizado',
            telefono='+56912345678'
        )

        # Assert
        assert proveedor_actualizado.razon_social == 'Nombre Actualizado'
        assert proveedor_actualizado.telefono == '+56912345678'

    def test_eliminar_proveedor_sin_ordenes_elimina_exitosamente(self):
        """
        GIVEN: Un proveedor sin órdenes de compra asociadas
        WHEN: Se elimina el proveedor
        THEN: El proveedor queda marcado como eliminado (soft delete)
        """
        # Arrange
        service = ProveedorService()
        proveedor = ProveedorFactory()

        # Act
        service.eliminar_proveedor(proveedor)

        # Assert
        proveedor.refresh_from_db()
        assert proveedor.eliminado is True
        assert proveedor.activo is False

    def test_eliminar_proveedor_con_ordenes_lanza_excepcion(self):
        """
        GIVEN: Un proveedor con órdenes de compra asociadas
        WHEN: Se intenta eliminar el proveedor
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = ProveedorService()
        proveedor = ProveedorFactory()
        OrdenCompraFactory(proveedor=proveedor)

        # Act & Assert
        with pytest.raises(ValidationError):
            service.eliminar_proveedor(proveedor)


# ==================== TESTS DE ORDEN COMPRA SERVICE ====================

@pytest.mark.django_db
class TestOrdenCompraService:
    """Tests para OrdenCompraService."""

    def test_calcular_totales_calcula_correctamente(self):
        """
        GIVEN: Un subtotal, impuesto y descuento
        WHEN: Se calculan los totales
        THEN: Los valores son correctos
        """
        # Arrange
        service = OrdenCompraService()
        subtotal = Decimal('10000.00')
        descuento = Decimal('500.00')

        # Act
        totales = service.calcular_totales(subtotal, descuento=descuento)

        # Assert
        assert totales['subtotal'] == Decimal('10000.00')
        assert totales['descuento'] == Decimal('500.00')
        # Impuesto: (10000 - 500) * 0.19 = 1805
        assert totales['impuesto'] == Decimal('1805.00')
        # Total: 10000 - 500 + 1805 = 11305
        assert totales['total'] == Decimal('11305.00')

    def test_crear_orden_compra_genera_numero_automatico(self, usuario_test, proveedor_activo, bodega_principal):
        """
        GIVEN: Datos para crear una orden sin número
        WHEN: Se crea la orden
        THEN: Se genera un número automáticamente
        """
        # Arrange
        service = OrdenCompraService()
        from datetime import date
        EstadoOrdenCompraFactory(codigo='PENDIENTE', es_inicial=True)

        # Act
        orden = service.crear_orden_compra(
            proveedor=proveedor_activo,
            bodega_destino=bodega_principal,
            solicitante=usuario_test,
            fecha_orden=date.today()
        )

        # Assert
        assert orden.numero is not None
        assert orden.numero.startswith('OC-')

    def test_crear_orden_con_proveedor_inactivo_lanza_excepcion(self, usuario_test, bodega_principal):
        """
        GIVEN: Un proveedor inactivo
        WHEN: Se intenta crear una orden con ese proveedor
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = OrdenCompraService()
        proveedor_inactivo = ProveedorFactory(activo=False)
        from datetime import date

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.crear_orden_compra(
                proveedor=proveedor_inactivo,
                bodega_destino=bodega_principal,
                solicitante=usuario_test,
                fecha_orden=date.today()
            )

        assert 'proveedor' in exc_info.value.message_dict

    def test_cambiar_estado_actualiza_estado_correctamente(self):
        """
        GIVEN: Una orden en estado pendiente
        WHEN: Se cambia el estado a aprobada
        THEN: El estado se actualiza correctamente
        """
        # Arrange
        service = OrdenCompraService()
        estado_pendiente = EstadoOrdenCompraFactory(codigo='PENDIENTE', es_final=False)
        estado_aprobada = EstadoOrdenCompraFactory(codigo='APROBADA', es_final=False)
        orden = OrdenCompraFactory(estado=estado_pendiente)
        usuario = UserFactory()

        # Act
        orden_actualizada = service.cambiar_estado(orden, estado_aprobada, usuario)

        # Assert
        assert orden_actualizada.estado.codigo == 'APROBADA'

    def test_cambiar_estado_orden_finalizada_lanza_excepcion(self):
        """
        GIVEN: Una orden en estado final
        WHEN: Se intenta cambiar el estado
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = OrdenCompraService()
        estado_finalizada = EstadoOrdenCompraFactory(codigo='FINALIZADA', es_final=True)
        estado_nueva = EstadoOrdenCompraFactory(codigo='NUEVA')
        orden = OrdenCompraFactory(estado=estado_finalizada)
        usuario = UserFactory()

        # Act & Assert
        with pytest.raises(ValidationError):
            service.cambiar_estado(orden, estado_nueva, usuario)

    def test_recalcular_totales_actualiza_orden_correctamente(self):
        """
        GIVEN: Una orden con detalles
        WHEN: Se recalculan los totales
        THEN: Los totales se actualizan correctamente
        """
        # Arrange
        service = OrdenCompraService()
        orden = OrdenCompraFactory(subtotal=Decimal('0'), impuesto=Decimal('0'), total=Decimal('0'))
        from apps.compras.tests.factories import DetalleOrdenCompraArticuloFactory
        DetalleOrdenCompraArticuloFactory(
            orden_compra=orden,
            cantidad=Decimal('10'),
            precio_unitario=Decimal('1000'),
            descuento=Decimal('0')
        )

        # Act
        orden_actualizada = service.recalcular_totales(orden)

        # Assert
        assert orden_actualizada.subtotal == Decimal('10000.00')
        assert orden_actualizada.impuesto > Decimal('0')
        assert orden_actualizada.total > orden_actualizada.subtotal


# ==================== TESTS DE RECEPCIÓN ARTÍCULO SERVICE ====================

@pytest.mark.django_db
class TestRecepcionArticuloService:
    """Tests para RecepcionArticuloService."""

    def test_crear_recepcion_genera_numero_automatico(self, usuario_test, bodega_principal):
        """
        GIVEN: Datos para crear una recepción sin número
        WHEN: Se crea la recepción
        THEN: Se genera un número automáticamente
        """
        # Arrange
        service = RecepcionArticuloService()
        EstadoRecepcionFactory(codigo='BORRADOR', es_inicial=True)

        # Act
        recepcion = service.crear_recepcion(
            recibido_por=usuario_test,
            bodega=bodega_principal
        )

        # Assert
        assert recepcion.numero is not None
        assert recepcion.numero.startswith('RART-')

    def test_crear_recepcion_sin_bodega_lanza_excepcion(self, usuario_test):
        """
        GIVEN: Intento de crear recepción de artículos sin bodega
        WHEN: Se llama a crear_recepcion
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = RecepcionArticuloService()
        EstadoRecepcionFactory(codigo='BORRADOR', es_inicial=True)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.crear_recepcion(
                recibido_por=usuario_test,
                bodega=None
            )

        assert 'bodega' in exc_info.value.message_dict

    def test_agregar_detalle_actualiza_stock_correctamente(
        self,
        recepcion_articulo_test,
        articulo_test
    ):
        """
        GIVEN: Una recepción y un artículo con stock inicial
        WHEN: Se agrega un detalle con cantidad
        THEN: El stock se actualiza correctamente
        """
        # Arrange
        service = RecepcionArticuloService()
        stock_inicial = articulo_test.stock_actual
        cantidad_recepcion = Decimal('50.00')

        # Act
        detalle = service.agregar_detalle(
            recepcion=recepcion_articulo_test,
            articulo=articulo_test,
            cantidad=cantidad_recepcion,
            actualizar_stock=True
        )

        # Assert
        articulo_test.refresh_from_db()
        assert articulo_test.stock_actual == stock_inicial + cantidad_recepcion
        assert detalle.cantidad == cantidad_recepcion

    def test_agregar_detalle_sin_actualizar_stock_no_modifica_stock(
        self,
        recepcion_articulo_test,
        articulo_test
    ):
        """
        GIVEN: Una recepción y un artículo
        WHEN: Se agrega detalle con actualizar_stock=False
        THEN: El stock NO se actualiza
        """
        # Arrange
        service = RecepcionArticuloService()
        stock_inicial = articulo_test.stock_actual

        # Act
        service.agregar_detalle(
            recepcion=recepcion_articulo_test,
            articulo=articulo_test,
            cantidad=Decimal('50.00'),
            actualizar_stock=False
        )

        # Assert
        articulo_test.refresh_from_db()
        assert articulo_test.stock_actual == stock_inicial

    def test_agregar_detalle_cantidad_negativa_lanza_excepcion(
        self,
        recepcion_articulo_test,
        articulo_test
    ):
        """
        GIVEN: Una recepción y artículo
        WHEN: Se intenta agregar detalle con cantidad <= 0
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = RecepcionArticuloService()

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.agregar_detalle(
                recepcion=recepcion_articulo_test,
                articulo=articulo_test,
                cantidad=Decimal('-10.00')
            )

        assert 'cantidad' in exc_info.value.message_dict

    def test_agregar_detalle_excede_stock_maximo_lanza_excepcion(self):
        """
        GIVEN: Un artículo con stock máximo definido
        WHEN: Se agrega una recepción que excede el stock máximo
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = RecepcionArticuloService()
        articulo = ArticuloFactory(
            stock_actual=Decimal('400.00'),
            stock_maximo=Decimal('500.00')
        )
        recepcion = RecepcionArticuloFactory()

        # Act & Assert
        with pytest.raises(ValidationError):
            service.agregar_detalle(
                recepcion=recepcion,
                articulo=articulo,
                cantidad=Decimal('200.00'),  # Excede stock máximo
                actualizar_stock=True
            )

    def test_agregar_detalle_recepcion_finalizada_lanza_excepcion(self):
        """
        GIVEN: Una recepción en estado final
        WHEN: Se intenta agregar un detalle
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = RecepcionArticuloService()
        estado_final = EstadoRecepcionFactory(codigo='COMPLETADA', es_final=True)
        recepcion = RecepcionArticuloFactory(estado=estado_final)
        articulo = ArticuloFactory()

        # Act & Assert
        with pytest.raises(ValidationError):
            service.agregar_detalle(
                recepcion=recepcion,
                articulo=articulo,
                cantidad=Decimal('10.00')
            )


# ==================== TESTS DE RECEPCIÓN ACTIVO SERVICE ====================

@pytest.mark.django_db
class TestRecepcionActivoService:
    """Tests para RecepcionActivoService."""

    def test_crear_recepcion_genera_numero_automatico(self, usuario_test):
        """
        GIVEN: Datos para crear una recepción de activos sin número
        WHEN: Se crea la recepción
        THEN: Se genera un número automáticamente
        """
        # Arrange
        service = RecepcionActivoService()
        EstadoRecepcionFactory(codigo='BORRADOR', es_inicial=True)

        # Act
        recepcion = service.crear_recepcion(
            recibido_por=usuario_test
        )

        # Assert
        assert recepcion.numero is not None
        assert recepcion.numero.startswith('RACT-')

    def test_agregar_detalle_activo_sin_serie_crea_exitosamente(
        self,
        recepcion_activo_test
    ):
        """
        GIVEN: Una recepción y un activo que NO requiere serie
        WHEN: Se agrega el detalle sin número de serie
        THEN: Se crea exitosamente
        """
        # Arrange
        service = RecepcionActivoService()
        from apps.compras.tests.factories import CategoriaActivoFactory, UnidadMedidaFactory, EstadoActivoFactory
        from apps.activos.models import Activo
        unidad = UnidadMedidaFactory(codigo='UND', nombre='Unidad', simbolo='UND')
        categoria = CategoriaActivoFactory()
        estado = EstadoActivoFactory()
        activo = Activo.objects.create(
            codigo='ACT-TEST',
            nombre='Silla',
            categoria=categoria,
            unidad_medida=unidad,
            estado=estado,
            requiere_serie=False
        )

        # Act
        detalle = service.agregar_detalle(
            recepcion=recepcion_activo_test,
            activo=activo,
            cantidad=Decimal('5.00')
        )

        # Assert
        assert detalle.id is not None
        assert detalle.cantidad == Decimal('5.00')

    def test_agregar_detalle_activo_con_serie_sin_proporcionar_serie_lanza_excepcion(
        self,
        recepcion_activo_test
    ):
        """
        GIVEN: Un activo que requiere número de serie
        WHEN: Se intenta agregar detalle sin número de serie
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = RecepcionActivoService()
        from apps.compras.tests.factories import CategoriaActivoFactory, UnidadMedidaFactory, EstadoActivoFactory
        from apps.activos.models import Activo
        unidad = UnidadMedidaFactory(codigo='UND2', nombre='Unidad', simbolo='UND')
        categoria = CategoriaActivoFactory()
        estado = EstadoActivoFactory()
        activo = Activo.objects.create(
            codigo='ACT-TEST-SER',
            nombre='Notebook',
            categoria=categoria,
            unidad_medida=unidad,
            estado=estado,
            requiere_serie=True
        )

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            service.agregar_detalle(
                recepcion=recepcion_activo_test,
                activo=activo,
                cantidad=Decimal('1.00')
            )

        assert 'numero_serie' in exc_info.value.message_dict

    def test_agregar_detalle_activo_con_serie_proporciona_serie_crea_exitosamente(
        self,
        recepcion_activo_test
    ):
        """
        GIVEN: Un activo que requiere serie y se proporciona
        WHEN: Se agrega el detalle
        THEN: Se crea exitosamente
        """
        # Arrange
        service = RecepcionActivoService()
        from apps.compras.tests.factories import CategoriaActivoFactory, UnidadMedidaFactory, EstadoActivoFactory
        from apps.activos.models import Activo
        unidad = UnidadMedidaFactory(codigo='UND3', nombre='Unidad', simbolo='UND')
        categoria = CategoriaActivoFactory()
        estado = EstadoActivoFactory()
        activo = Activo.objects.create(
            codigo='ACT-TEST-SER2',
            nombre='Laptop',
            categoria=categoria,
            unidad_medida=unidad,
            estado=estado,
            requiere_serie=True
        )

        # Act
        detalle = service.agregar_detalle(
            recepcion=recepcion_activo_test,
            activo=activo,
            cantidad=Decimal('1.00'),
            numero_serie='SN-123456789'
        )

        # Assert
        assert detalle.numero_serie == 'SN-123456789'

    def test_agregar_detalle_no_actualiza_stock(self, recepcion_activo_test):
        """
        GIVEN: Una recepción de activos
        WHEN: Se agrega un detalle
        THEN: NO se actualiza stock (los activos no manejan stock)
        """
        # Arrange
        service = RecepcionActivoService()
        activo = ActivoFactory(requiere_serie=False)

        # Act
        detalle = service.agregar_detalle(
            recepcion=recepcion_activo_test,
            activo=activo,
            cantidad=Decimal('3.00')
        )

        # Assert
        assert detalle.id is not None
        # Los activos no tienen atributo stock_actual
        assert not hasattr(activo, 'stock_actual')


# ==================== TESTS DE CASOS EDGE ====================

@pytest.mark.django_db
class TestServicesEdgeCases:
    """Tests de casos edge y límite."""

    def test_crear_orden_sin_estado_inicial_configurado_lanza_excepcion(
        self,
        usuario_test,
        proveedor_activo,
        bodega_principal
    ):
        """
        GIVEN: Sistema sin estado inicial configurado
        WHEN: Se intenta crear una orden
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = OrdenCompraService()
        from datetime import date
        # No se crea estado inicial

        # Act & Assert
        with pytest.raises(ValidationError):
            service.crear_orden_compra(
                proveedor=proveedor_activo,
                bodega_destino=bodega_principal,
                solicitante=usuario_test,
                fecha_orden=date.today()
            )

    def test_crear_recepcion_sin_estado_inicial_lanza_excepcion(self, usuario_test, bodega_principal):
        """
        GIVEN: Sistema sin estado inicial de recepción
        WHEN: Se intenta crear una recepción
        THEN: Se lanza ValidationError
        """
        # Arrange
        service = RecepcionArticuloService()
        # No se crea estado inicial

        # Act & Assert
        with pytest.raises(ValidationError):
            service.crear_recepcion(
                recibido_por=usuario_test,
                bodega=bodega_principal
            )

    def test_calcular_totales_con_descuento_mayor_que_subtotal_calcula_correctamente(self):
        """
        GIVEN: Descuento mayor que subtotal (caso edge)
        WHEN: Se calculan totales
        THEN: Se calcula correctamente (resultado puede ser negativo o cero)
        """
        # Arrange
        service = OrdenCompraService()

        # Act
        totales = service.calcular_totales(
            subtotal=Decimal('100.00'),
            descuento=Decimal('150.00')
        )

        # Assert
        # Impuesto: (100 - 150) * 0.19 = -9.50
        # Total: 100 - 150 + (-9.50) = -59.50
        assert totales['impuesto'] == Decimal('-9.50')
        assert totales['total'] == Decimal('-59.50')
