"""
Tests para formularios del módulo de compras.

Valida formularios, validaciones personalizadas y limpieza de datos.
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from apps.compras.forms import (
    ProveedorForm, OrdenCompraForm,
    DetalleOrdenCompraArticuloForm, DetalleOrdenCompraActivoForm,
    RecepcionArticuloForm, DetalleRecepcionArticuloForm,
    RecepcionActivoForm, DetalleRecepcionActivoForm
)
from apps.compras.tests.factories import (
    ProveedorFactory, EstadoOrdenCompraFactory,
    BodegaFactory, ArticuloFactory, ActivoFactory,
    OrdenCompraFactory, TipoRecepcionFactory,
    EstadoRecepcionFactory
)


# ==================== TESTS DE PROVEEDOR FORM ====================

@pytest.mark.django_db
class TestProveedorForm:
    """Tests para ProveedorForm."""

    def test_form_valido_guarda_correctamente(self):
        """
        GIVEN: Datos válidos de proveedor
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'rut': '76.123.456-7',
            'razon_social': 'Test S.A.',
            'direccion': 'Calle Test 123',
            'email': 'test@example.com',
            'condicion_pago': 'Contado',
            'dias_credito': 0,
            'activo': True
        }

        # Act
        form = ProveedorForm(data=data)

        # Assert
        assert form.is_valid()

    def test_form_rut_duplicado_invalido(self):
        """
        GIVEN: Un RUT ya existente
        WHEN: Se intenta crear otro proveedor con ese RUT
        THEN: El formulario es inválido
        """
        # Arrange
        rut = '76.123.456-7'
        ProveedorFactory(rut=rut)
        data = {
            'rut': rut,
            'razon_social': 'Otro Proveedor',
            'direccion': 'Otra Calle'
        }

        # Act
        form = ProveedorForm(data=data)

        # Assert
        assert not form.is_valid()
        assert 'rut' in form.errors

    def test_form_email_invalido_muestra_error(self):
        """
        GIVEN: Un email inválido
        WHEN: Se envía el formulario
        THEN: El formulario es inválido
        """
        # Arrange
        data = {
            'rut': '76.123.456-7',
            'razon_social': 'Test S.A.',
            'direccion': 'Calle Test 123',
            'email': 'email_invalido',
            'activo': True
        }

        # Act
        form = ProveedorForm(data=data)

        # Assert
        assert not form.is_valid()
        assert 'email' in form.errors


# ==================== TESTS DE ORDEN COMPRA FORM ====================

@pytest.mark.django_db
class TestOrdenCompraForm:
    """Tests para OrdenCompraForm."""

    def test_form_valido_guarda_correctamente(
        self,
        proveedor_activo,
        bodega_principal,
        estado_orden_pendiente
    ):
        """
        GIVEN: Datos válidos de orden de compra
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'fecha_orden': date.today(),
            'fecha_entrega_esperada': date.today() + timedelta(days=7),
            'proveedor': proveedor_activo.id,
            'bodega_destino': bodega_principal.id,
            'estado': estado_orden_pendiente.id,
            'observaciones': 'Observaciones de test'
        }

        # Act
        form = OrdenCompraForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_form_fecha_entrega_anterior_fecha_orden_invalido(
        self,
        proveedor_activo,
        bodega_principal,
        estado_orden_pendiente
    ):
        """
        GIVEN: Fecha de entrega anterior a fecha de orden
        WHEN: Se envía el formulario
        THEN: El formulario es inválido
        """
        # Arrange
        data = {
            'fecha_orden': date.today(),
            'fecha_entrega_esperada': date.today() - timedelta(days=1),
            'proveedor': proveedor_activo.id,
            'bodega_destino': bodega_principal.id,
            'estado': estado_orden_pendiente.id
        }

        # Act
        form = OrdenCompraForm(data=data)

        # Assert
        assert not form.is_valid()
        assert 'fecha_entrega_esperada' in form.errors


# ==================== TESTS DE DETALLE ORDEN COMPRA ARTICULO FORM ====================

@pytest.mark.django_db
class TestDetalleOrdenCompraArticuloForm:
    """Tests para DetalleOrdenCompraArticuloForm."""

    def test_form_valido_guarda_correctamente(self, articulo_test):
        """
        GIVEN: Datos válidos de detalle de artículo
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'articulo': articulo_test.id,
            'cantidad': Decimal('10.00'),
            'precio_unitario': Decimal('1000.00'),
            'descuento': Decimal('0.00'),
            'observaciones': 'Test'
        }

        # Act
        form = DetalleOrdenCompraArticuloForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_form_descuento_mayor_que_subtotal_invalido(self, articulo_test):
        """
        GIVEN: Descuento mayor que subtotal
        WHEN: Se envía el formulario
        THEN: El formulario es inválido
        """
        # Arrange
        data = {
            'articulo': articulo_test.id,
            'cantidad': Decimal('10.00'),
            'precio_unitario': Decimal('100.00'),
            'descuento': Decimal('2000.00'),  # Mayor que 10 * 100 = 1000
            'observaciones': 'Test'
        }

        # Act
        form = DetalleOrdenCompraArticuloForm(data=data)

        # Assert
        assert not form.is_valid()
        assert 'descuento' in form.errors


# ==================== TESTS DE DETALLE ORDEN COMPRA ACTIVO FORM ====================

@pytest.mark.django_db
class TestDetalleOrdenCompraActivoForm:
    """Tests para DetalleOrdenCompraActivoForm."""

    def test_form_valido_guarda_correctamente(self, activo_test):
        """
        GIVEN: Datos válidos de detalle de activo
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'activo': activo_test.id,
            'cantidad': Decimal('5.00'),
            'precio_unitario': Decimal('50000.00'),
            'descuento': Decimal('0.00'),
            'observaciones': 'Test'
        }

        # Act
        form = DetalleOrdenCompraActivoForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_form_descuento_mayor_que_subtotal_invalido(self, activo_test):
        """
        GIVEN: Descuento mayor que subtotal
        WHEN: Se envía el formulario
        THEN: El formulario es inválido
        """
        # Arrange
        data = {
            'activo': activo_test.id,
            'cantidad': Decimal('2.00'),
            'precio_unitario': Decimal('10000.00'),
            'descuento': Decimal('30000.00'),  # Mayor que 2 * 10000 = 20000
            'observaciones': 'Test'
        }

        # Act
        form = DetalleOrdenCompraActivoForm(data=data)

        # Assert
        assert not form.is_valid()
        assert 'descuento' in form.errors


# ==================== TESTS DE RECEPCIÓN ARTÍCULO FORM ====================

@pytest.mark.django_db
class TestRecepcionArticuloForm:
    """Tests para RecepcionArticuloForm."""

    def test_form_valido_sin_orden_compra_guarda_correctamente(
        self,
        bodega_principal,
        tipo_recepcion_sin_orden
    ):
        """
        GIVEN: Datos válidos de recepción sin orden de compra
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'tipo': tipo_recepcion_sin_orden.id,
            'bodega': bodega_principal.id,
            'documento_referencia': 'GUIA-12345',
            'observaciones': 'Test'
        }

        # Act
        form = RecepcionArticuloForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_form_tipo_requiere_orden_sin_orden_invalido(
        self,
        bodega_principal,
        tipo_recepcion_con_orden
    ):
        """
        GIVEN: Tipo de recepción que requiere orden pero no se proporciona
        WHEN: Se envía el formulario
        THEN: El formulario es inválido
        """
        # Arrange
        data = {
            'tipo': tipo_recepcion_con_orden.id,
            'bodega': bodega_principal.id,
            'documento_referencia': 'GUIA-12345'
        }

        # Act
        form = RecepcionArticuloForm(data=data)

        # Assert
        assert not form.is_valid()
        assert 'orden_compra' in form.errors

    def test_form_tipo_requiere_orden_con_orden_valido(
        self,
        bodega_principal,
        tipo_recepcion_con_orden,
        orden_compra_test
    ):
        """
        GIVEN: Tipo que requiere orden y se proporciona orden
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'tipo': tipo_recepcion_con_orden.id,
            'orden_compra': orden_compra_test.id,
            'bodega': bodega_principal.id,
            'documento_referencia': 'GUIA-12345'
        }

        # Act
        form = RecepcionArticuloForm(data=data)

        # Assert
        assert form.is_valid(), form.errors


# ==================== TESTS DE DETALLE RECEPCIÓN ARTÍCULO FORM ====================

@pytest.mark.django_db
class TestDetalleRecepcionArticuloForm:
    """Tests para DetalleRecepcionArticuloForm."""

    def test_form_valido_guarda_correctamente(self, articulo_test):
        """
        GIVEN: Datos válidos de detalle de recepción
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'articulo': articulo_test.id,
            'cantidad': Decimal('50.00'),
            'lote': 'LOTE-001',
            'fecha_vencimiento': date.today() + timedelta(days=365),
            'observaciones': 'Test'
        }

        # Act
        form = DetalleRecepcionArticuloForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_form_sin_lote_ni_fecha_valido(self, articulo_test):
        """
        GIVEN: Detalle sin lote ni fecha de vencimiento (opcionales)
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'articulo': articulo_test.id,
            'cantidad': Decimal('50.00')
        }

        # Act
        form = DetalleRecepcionArticuloForm(data=data)

        # Assert
        assert form.is_valid(), form.errors


# ==================== TESTS DE RECEPCIÓN ACTIVO FORM ====================

@pytest.mark.django_db
class TestRecepcionActivoForm:
    """Tests para RecepcionActivoForm."""

    def test_form_valido_sin_orden_compra_guarda_correctamente(
        self,
        tipo_recepcion_sin_orden
    ):
        """
        GIVEN: Datos válidos de recepción de activos sin orden
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'tipo': tipo_recepcion_sin_orden.id,
            'documento_referencia': 'GUIA-67890',
            'observaciones': 'Test activos'
        }

        # Act
        form = RecepcionActivoForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_form_tipo_requiere_orden_sin_orden_invalido(
        self,
        tipo_recepcion_con_orden
    ):
        """
        GIVEN: Tipo que requiere orden pero no se proporciona
        WHEN: Se envía el formulario
        THEN: El formulario es inválido
        """
        # Arrange
        data = {
            'tipo': tipo_recepcion_con_orden.id,
            'documento_referencia': 'GUIA-67890'
        }

        # Act
        form = RecepcionActivoForm(data=data)

        # Assert
        assert not form.is_valid()
        assert 'orden_compra' in form.errors


# ==================== TESTS DE DETALLE RECEPCIÓN ACTIVO FORM ====================

@pytest.mark.django_db
class TestDetalleRecepcionActivoForm:
    """Tests para DetalleRecepcionActivoForm."""

    def test_form_valido_con_serie_guarda_correctamente(self, activo_test):
        """
        GIVEN: Datos válidos de detalle de recepción de activos
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'activo': activo_test.id,
            'cantidad': Decimal('1.00'),
            'numero_serie': 'SN-123456789',
            'observaciones': 'Test activo'
        }

        # Act
        form = DetalleRecepcionActivoForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_form_sin_serie_valido(self, activo_sin_serie):
        """
        GIVEN: Detalle sin número de serie (opcional)
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'activo': activo_sin_serie.id,
            'cantidad': Decimal('3.00')
        }

        # Act
        form = DetalleRecepcionActivoForm(data=data)

        # Assert
        assert form.is_valid(), form.errors


# ==================== TESTS DE CASOS EDGE EN FORMS ====================

@pytest.mark.django_db
class TestFormsEdgeCases:
    """Tests de casos edge en formularios."""

    def test_proveedor_form_edicion_mismo_rut_valido(self):
        """
        GIVEN: Edición de proveedor con su propio RUT
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        proveedor = ProveedorFactory(rut='76.123.456-7')
        data = {
            'rut': '76.123.456-7',  # Mismo RUT
            'razon_social': 'Nombre Actualizado',
            'direccion': 'Nueva Dirección',
            'condicion_pago': 'Contado',
            'dias_credito': 0
        }

        # Act
        form = ProveedorForm(data=data, instance=proveedor)

        # Assert
        assert form.is_valid(), form.errors

    def test_detalle_articulo_cantidad_minima_valido(self, articulo_test):
        """
        GIVEN: Cantidad mínima permitida (1.00)
        WHEN: Se envía el formulario
        THEN: El formulario es válido
        """
        # Arrange
        data = {
            'articulo': articulo_test.id,
            'cantidad': Decimal('1.00'),
            'precio_unitario': Decimal('100.00'),
            'descuento': Decimal('0.00')
        }

        # Act
        form = DetalleOrdenCompraArticuloForm(data=data)

        # Assert
        assert form.is_valid(), form.errors

    def test_orden_compra_fechas_iguales_valido(
        self,
        proveedor_activo,
        bodega_principal,
        estado_orden_pendiente
    ):
        """
        GIVEN: Fecha de orden y entrega iguales
        WHEN: Se envía el formulario
        THEN: El formulario es válido (mismo día es permitido)
        """
        # Arrange
        hoy = date.today()
        data = {
            'fecha_orden': hoy,
            'fecha_entrega_esperada': hoy,
            'proveedor': proveedor_activo.id,
            'bodega_destino': bodega_principal.id,
            'estado': estado_orden_pendiente.id
        }

        # Act
        form = OrdenCompraForm(data=data)

        # Assert
        assert form.is_valid(), form.errors
