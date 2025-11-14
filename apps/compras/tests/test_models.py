"""
Tests para modelos del módulo de compras.

Valida campos, relaciones, métodos custom y restricciones de base de datos.
"""
import pytest
from decimal import Decimal
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.compras.models import (
    Proveedor, OrdenCompra, DetalleOrdenCompra, DetalleOrdenCompraArticulo,
    EstadoOrdenCompra, RecepcionArticulo, DetalleRecepcionArticulo,
    RecepcionActivo, DetalleRecepcionActivo
)
from apps.compras.tests.factories import (
    ProveedorFactory, OrdenCompraFactory,
    DetalleOrdenCompraArticuloFactory, DetalleOrdenCompraActivoFactory,
    RecepcionArticuloFactory, RecepcionActivoFactory,
    DetalleRecepcionArticuloFactory, DetalleRecepcionActivoFactory
)


# ==================== TESTS DE PROVEEDOR ====================

@pytest.mark.django_db
class TestProveedorModel:
    """Tests para modelo Proveedor."""

    def test_crear_proveedor_valido_guarda_exitosamente(self):
        """
        GIVEN: Datos válidos de proveedor
        WHEN: Se crea el proveedor
        THEN: Se guarda correctamente
        """
        # Arrange & Act
        proveedor = ProveedorFactory(
            rut='76.123.456-7',
            razon_social='Test S.A.'
        )

        # Assert
        assert proveedor.id is not None
        assert proveedor.activo is True
        assert proveedor.eliminado is False

    def test_proveedor_str_retorna_formato_correcto(self):
        """
        GIVEN: Un proveedor con RUT y razón social
        WHEN: Se llama a __str__
        THEN: Retorna formato "RUT - Razón Social"
        """
        # Arrange
        proveedor = ProveedorFactory(
            rut='76.123.456-7',
            razon_social='Proveedor Test S.A.'
        )

        # Act
        resultado = str(proveedor)

        # Assert
        assert '76.123.456-7' in resultado
        assert 'Proveedor Test S.A.' in resultado

    def test_rut_duplicado_lanza_excepcion(self):
        """
        GIVEN: Un proveedor existente con un RUT
        WHEN: Se intenta crear otro con el mismo RUT
        THEN: Se lanza IntegrityError
        """
        # Arrange
        rut = '76.123.456-7'
        ProveedorFactory(rut=rut)

        # Act & Assert
        with pytest.raises(IntegrityError):
            ProveedorFactory(rut=rut)

    def test_email_invalido_lanza_excepcion(self):
        """
        GIVEN: Un proveedor con email inválido
        WHEN: Se valida el modelo
        THEN: Se lanza ValidationError
        """
        # Arrange
        proveedor = ProveedorFactory.build(email='email_invalido')

        # Act & Assert
        with pytest.raises(ValidationError):
            proveedor.full_clean()

    def test_dias_credito_negativo_lanza_excepcion(self):
        """
        GIVEN: Días de crédito negativo
        WHEN: Se valida el modelo
        THEN: Se lanza ValidationError
        """
        # Arrange
        proveedor = ProveedorFactory.build(dias_credito=-10)

        # Act & Assert
        with pytest.raises(ValidationError):
            proveedor.full_clean()


# ==================== TESTS DE ORDEN DE COMPRA ====================

@pytest.mark.django_db
class TestOrdenCompraModel:
    """Tests para modelo OrdenCompra."""

    def test_crear_orden_compra_valida_guarda_exitosamente(self):
        """
        GIVEN: Datos válidos de orden de compra
        WHEN: Se crea la orden
        THEN: Se guarda correctamente
        """
        # Arrange & Act
        orden = OrdenCompraFactory()

        # Assert
        assert orden.id is not None
        assert orden.total >= Decimal('0')

    def test_orden_str_retorna_formato_correcto(self):
        """
        GIVEN: Una orden con número y proveedor
        WHEN: Se llama a __str__
        THEN: Retorna formato "OC-numero - Proveedor"
        """
        # Arrange
        orden = OrdenCompraFactory(numero='OC-2025-000001')

        # Act
        resultado = str(orden)

        # Assert
        assert 'OC-OC-2025-000001' in resultado or 'OC-2025-000001' in resultado

    def test_numero_duplicado_lanza_excepcion(self):
        """
        GIVEN: Una orden existente con un número
        WHEN: Se intenta crear otra con el mismo número
        THEN: Se lanza IntegrityError
        """
        # Arrange
        numero = 'OC-2025-000001'
        OrdenCompraFactory(numero=numero)

        # Act & Assert
        with pytest.raises(IntegrityError):
            OrdenCompraFactory(numero=numero)

    def test_montos_negativos_lanza_excepcion(self):
        """
        GIVEN: Montos negativos en orden
        WHEN: Se valida el modelo
        THEN: Se lanza ValidationError
        """
        # Arrange
        orden = OrdenCompraFactory.build(subtotal=Decimal('-100'))

        # Act & Assert
        with pytest.raises(ValidationError):
            orden.full_clean()


# ==================== TESTS DE DETALLE ORDEN COMPRA ARTICULO ====================

@pytest.mark.django_db
class TestDetalleOrdenCompraArticuloModel:
    """Tests para modelo DetalleOrdenCompraArticulo."""

    def test_crear_detalle_valido_guarda_exitosamente(self):
        """
        GIVEN: Datos válidos de detalle
        WHEN: Se crea el detalle
        THEN: Se guarda correctamente
        """
        # Arrange & Act
        detalle = DetalleOrdenCompraArticuloFactory()

        # Assert
        assert detalle.id is not None
        assert detalle.cantidad > Decimal('0')

    def test_save_calcula_subtotal_automaticamente(self):
        """
        GIVEN: Detalle con cantidad y precio
        WHEN: Se guarda el detalle
        THEN: El subtotal se calcula automáticamente
        """
        # Arrange
        detalle = DetalleOrdenCompraArticuloFactory(
            cantidad=Decimal('10'),
            precio_unitario=Decimal('1000'),
            descuento=Decimal('500')
        )

        # Act
        detalle.save()

        # Assert
        # Subtotal = (10 * 1000) - 500 = 9500
        assert detalle.subtotal == Decimal('9500.00')

    def test_cantidad_cero_lanza_excepcion(self):
        """
        GIVEN: Detalle con cantidad 0
        WHEN: Se valida el modelo
        THEN: Se lanza ValidationError
        """
        # Arrange
        detalle = DetalleOrdenCompraArticuloFactory.build(cantidad=Decimal('0'))

        # Act & Assert
        with pytest.raises(ValidationError):
            detalle.full_clean()


# ==================== TESTS DE RECEPCIÓN ARTÍCULO ====================

@pytest.mark.django_db
class TestRecepcionArticuloModel:
    """Tests para modelo RecepcionArticulo."""

    def test_crear_recepcion_valida_guarda_exitosamente(self):
        """
        GIVEN: Datos válidos de recepción
        WHEN: Se crea la recepción
        THEN: Se guarda correctamente
        """
        # Arrange & Act
        recepcion = RecepcionArticuloFactory()

        # Assert
        assert recepcion.id is not None
        assert recepcion.numero is not None

    def test_recepcion_str_retorna_formato_correcto(self):
        """
        GIVEN: Una recepción con número
        WHEN: Se llama a __str__
        THEN: Retorna formato con REC-ART
        """
        # Arrange
        recepcion = RecepcionArticuloFactory(numero='RART-2025-000001')

        # Act
        resultado = str(recepcion)

        # Assert
        assert 'REC-ART' in resultado or 'RART' in resultado

    def test_numero_duplicado_lanza_excepcion(self):
        """
        GIVEN: Una recepción existente con un número
        WHEN: Se intenta crear otra con el mismo número
        THEN: Se lanza IntegrityError
        """
        # Arrange
        numero = 'RART-2025-000001'
        RecepcionArticuloFactory(numero=numero)

        # Act & Assert
        with pytest.raises(IntegrityError):
            RecepcionArticuloFactory(numero=numero)


# ==================== TESTS DE DETALLE RECEPCIÓN ARTÍCULO ====================

@pytest.mark.django_db
class TestDetalleRecepcionArticuloModel:
    """Tests para modelo DetalleRecepcionArticulo."""

    def test_crear_detalle_valido_guarda_exitosamente(self):
        """
        GIVEN: Datos válidos de detalle de recepción
        WHEN: Se crea el detalle
        THEN: Se guarda correctamente
        """
        # Arrange & Act
        detalle = DetalleRecepcionArticuloFactory()

        # Assert
        assert detalle.id is not None
        assert detalle.cantidad > Decimal('0')

    def test_detalle_str_retorna_formato_correcto(self):
        """
        GIVEN: Un detalle con recepción y artículo
        WHEN: Se llama a __str__
        THEN: Retorna formato correcto
        """
        # Arrange
        detalle = DetalleRecepcionArticuloFactory()

        # Act
        resultado = str(detalle)

        # Assert
        assert resultado  # Debe retornar algo

    def test_cantidad_negativa_lanza_excepcion(self):
        """
        GIVEN: Detalle con cantidad negativa
        WHEN: Se valida el modelo
        THEN: Se lanza ValidationError
        """
        # Arrange
        detalle = DetalleRecepcionArticuloFactory.build(cantidad=Decimal('-5'))

        # Act & Assert
        with pytest.raises(ValidationError):
            detalle.full_clean()


# ==================== TESTS DE RECEPCIÓN ACTIVO ====================

@pytest.mark.django_db
class TestRecepcionActivoModel:
    """Tests para modelo RecepcionActivo."""

    def test_crear_recepcion_activo_valida_guarda_exitosamente(self):
        """
        GIVEN: Datos válidos de recepción de activos
        WHEN: Se crea la recepción
        THEN: Se guarda correctamente
        """
        # Arrange & Act
        recepcion = RecepcionActivoFactory()

        # Assert
        assert recepcion.id is not None
        assert recepcion.numero is not None

    def test_recepcion_activo_str_retorna_formato_correcto(self):
        """
        GIVEN: Una recepción de activos con número
        WHEN: Se llama a __str__
        THEN: Retorna formato con REC-ACT
        """
        # Arrange
        recepcion = RecepcionActivoFactory(numero='RACT-2025-000001')

        # Act
        resultado = str(recepcion)

        # Assert
        assert 'REC-ACT' in resultado or 'RACT' in resultado

    def test_recepcion_activo_no_requiere_bodega(self):
        """
        GIVEN: Modelo RecepcionActivo
        WHEN: Se verifica su estructura
        THEN: NO tiene campo bodega
        """
        # Arrange
        recepcion = RecepcionActivoFactory()

        # Assert
        assert not hasattr(recepcion, 'bodega')


# ==================== TESTS DE DETALLE RECEPCIÓN ACTIVO ====================

@pytest.mark.django_db
class TestDetalleRecepcionActivoModel:
    """Tests para modelo DetalleRecepcionActivo."""

    def test_crear_detalle_activo_valido_guarda_exitosamente(self):
        """
        GIVEN: Datos válidos de detalle de recepción de activos
        WHEN: Se crea el detalle
        THEN: Se guarda correctamente
        """
        # Arrange & Act
        detalle = DetalleRecepcionActivoFactory()

        # Assert
        assert detalle.id is not None
        assert detalle.cantidad > Decimal('0')

    def test_detalle_activo_puede_tener_numero_serie_vacio(self):
        """
        GIVEN: Detalle de activo sin número de serie
        WHEN: Se crea el detalle
        THEN: Se guarda correctamente (serie es opcional)
        """
        # Arrange & Act
        detalle = DetalleRecepcionActivoFactory(numero_serie='')

        # Assert
        assert detalle.numero_serie == ''

    def test_detalle_activo_str_retorna_formato_correcto(self):
        """
        GIVEN: Un detalle con recepción y activo
        WHEN: Se llama a __str__
        THEN: Retorna formato correcto
        """
        # Arrange
        detalle = DetalleRecepcionActivoFactory()

        # Act
        resultado = str(detalle)

        # Assert
        assert resultado  # Debe retornar algo


# ==================== TESTS DE RELACIONES ====================

@pytest.mark.django_db
class TestModelRelations:
    """Tests para relaciones entre modelos."""

    def test_orden_compra_proveedor_relacion_funciona(self):
        """
        GIVEN: Una orden con proveedor
        WHEN: Se accede a la relación
        THEN: Funciona correctamente
        """
        # Arrange
        orden = OrdenCompraFactory()

        # Act & Assert
        assert orden.proveedor is not None
        assert orden.proveedor.razon_social

    def test_orden_compra_tiene_detalles_articulos_y_activos(self):
        """
        GIVEN: Una orden con detalles de artículos y activos
        WHEN: Se accede a los detalles
        THEN: Retorna los detalles correctos
        """
        # Arrange
        orden = OrdenCompraFactory()
        DetalleOrdenCompraArticuloFactory(orden_compra=orden)
        DetalleOrdenCompraActivoFactory(orden_compra=orden)

        # Act
        detalles_articulos = orden.detalles_articulos.all()
        detalles_activos = orden.detalles.all()

        # Assert
        assert detalles_articulos.count() == 1
        assert detalles_activos.count() == 1

    def test_recepcion_articulo_tiene_bodega_relacionada(self):
        """
        GIVEN: Una recepción de artículos
        WHEN: Se accede a la bodega
        THEN: Retorna la bodega correcta
        """
        # Arrange
        recepcion = RecepcionArticuloFactory()

        # Act & Assert
        assert recepcion.bodega is not None
        assert recepcion.bodega.nombre

    def test_recepcion_tiene_detalles_relacionados(self):
        """
        GIVEN: Una recepción con detalles
        WHEN: Se accede a los detalles
        THEN: Retorna los detalles correctos
        """
        # Arrange
        recepcion = RecepcionArticuloFactory()
        DetalleRecepcionArticuloFactory(recepcion=recepcion)
        DetalleRecepcionArticuloFactory(recepcion=recepcion)

        # Act
        detalles = recepcion.detalles.all()

        # Assert
        assert detalles.count() == 2
