"""
Tests para la capa de repositorios del módulo de compras.

Valida métodos de consulta, filtros y optimización de queries.
"""
import pytest
from apps.compras.repositories import (
    ProveedorRepository,
    EstadoOrdenCompraRepository,
    OrdenCompraRepository,
    EstadoRecepcionRepository,
    RecepcionArticuloRepository,
    RecepcionActivoRepository,
    DetalleRecepcionArticuloRepository
)
from apps.compras.tests.factories import (
    ProveedorFactory, EstadoOrdenCompraFactory,
    OrdenCompraFactory, EstadoRecepcionFactory,
    RecepcionArticuloFactory, RecepcionActivoFactory,
    BodegaFactory, UserFactory, DetalleRecepcionArticuloFactory
)


# ==================== TESTS DE PROVEEDOR REPOSITORY ====================

@pytest.mark.django_db
class TestProveedorRepository:
    """Tests para ProveedorRepository."""

    def test_get_all_retorna_proveedores_no_eliminados(self):
        """
        GIVEN: Proveedores eliminados y no eliminados
        WHEN: Se llama a get_all
        THEN: Retorna solo proveedores no eliminados
        """
        # Arrange
        proveedor_activo = ProveedorFactory(eliminado=False)
        proveedor_eliminado = ProveedorFactory(eliminado=True)
        repo = ProveedorRepository()

        # Act
        proveedores = repo.get_all()

        # Assert
        assert proveedor_activo in proveedores
        assert proveedor_eliminado not in proveedores

    def test_get_active_retorna_solo_proveedores_activos(self):
        """
        GIVEN: Proveedores activos e inactivos
        WHEN: Se llama a get_active
        THEN: Retorna solo proveedores activos
        """
        # Arrange
        proveedor_activo = ProveedorFactory(activo=True, eliminado=False)
        proveedor_inactivo = ProveedorFactory(activo=False, eliminado=False)
        repo = ProveedorRepository()

        # Act
        proveedores = repo.get_active()

        # Assert
        assert proveedor_activo in proveedores
        assert proveedor_inactivo not in proveedores

    def test_get_by_id_retorna_proveedor_correcto(self):
        """
        GIVEN: Un proveedor con ID específico
        WHEN: Se busca por ID
        THEN: Retorna el proveedor correcto
        """
        # Arrange
        proveedor = ProveedorFactory()
        repo = ProveedorRepository()

        # Act
        resultado = repo.get_by_id(proveedor.id)

        # Assert
        assert resultado == proveedor

    def test_get_by_id_proveedor_eliminado_retorna_none(self):
        """
        GIVEN: Un proveedor eliminado
        WHEN: Se busca por ID
        THEN: Retorna None
        """
        # Arrange
        proveedor = ProveedorFactory(eliminado=True)
        repo = ProveedorRepository()

        # Act
        resultado = repo.get_by_id(proveedor.id)

        # Assert
        assert resultado is None

    def test_get_by_rut_retorna_proveedor_correcto(self):
        """
        GIVEN: Un proveedor con RUT específico
        WHEN: Se busca por RUT
        THEN: Retorna el proveedor correcto
        """
        # Arrange
        rut = '76.123.456-7'
        proveedor = ProveedorFactory(rut=rut)
        repo = ProveedorRepository()

        # Act
        resultado = repo.get_by_rut(rut)

        # Assert
        assert resultado == proveedor

    def test_search_busca_por_rut_razon_social_y_nombre_fantasia(self):
        """
        GIVEN: Proveedores con diferentes datos
        WHEN: Se busca con un query
        THEN: Retorna proveedores que coinciden en RUT, razón social o nombre fantasía
        """
        # Arrange
        proveedor1 = ProveedorFactory(razon_social='Empresa ABC', rut='76.111.111-1')
        proveedor2 = ProveedorFactory(nombre_fantasia='ABC Corp', rut='76.222.222-2')
        proveedor3 = ProveedorFactory(razon_social='XYZ Ltda', rut='76.333.333-3')
        repo = ProveedorRepository()

        # Act
        resultados = repo.search('ABC')

        # Assert
        assert proveedor1 in resultados
        assert proveedor2 in resultados
        assert proveedor3 not in resultados

    def test_exists_by_rut_retorna_true_si_existe(self):
        """
        GIVEN: Un proveedor con RUT específico
        WHEN: Se verifica existencia del RUT
        THEN: Retorna True
        """
        # Arrange
        rut = '76.123.456-7'
        ProveedorFactory(rut=rut)
        repo = ProveedorRepository()

        # Act
        existe = repo.exists_by_rut(rut)

        # Assert
        assert existe is True

    def test_exists_by_rut_excluye_id_correctamente(self):
        """
        GIVEN: Un proveedor con RUT y su ID
        WHEN: Se verifica existencia excluyendo su propio ID
        THEN: Retorna False
        """
        # Arrange
        proveedor = ProveedorFactory(rut='76.123.456-7')
        repo = ProveedorRepository()

        # Act
        existe = repo.exists_by_rut('76.123.456-7', exclude_id=proveedor.id)

        # Assert
        assert existe is False


# ==================== TESTS DE ESTADO ORDEN COMPRA REPOSITORY ====================

@pytest.mark.django_db
class TestEstadoOrdenCompraRepository:
    """Tests para EstadoOrdenCompraRepository."""

    def test_get_all_retorna_estados_activos(self):
        """
        GIVEN: Estados activos e inactivos
        WHEN: Se llama a get_all
        THEN: Retorna solo estados activos
        """
        # Arrange
        estado_activo = EstadoOrdenCompraFactory(activo=True)
        estado_inactivo = EstadoOrdenCompraFactory(activo=False)
        repo = EstadoOrdenCompraRepository()

        # Act
        estados = repo.get_all()

        # Assert
        assert estado_activo in estados
        assert estado_inactivo not in estados

    def test_get_by_codigo_retorna_estado_correcto(self):
        """
        GIVEN: Un estado con código específico
        WHEN: Se busca por código
        THEN: Retorna el estado correcto
        """
        # Arrange
        estado = EstadoOrdenCompraFactory(codigo='PENDIENTE')
        repo = EstadoOrdenCompraRepository()

        # Act
        resultado = repo.get_by_codigo('PENDIENTE')

        # Assert
        assert resultado == estado

    def test_get_inicial_retorna_estado_inicial(self):
        """
        GIVEN: Estados con uno marcado como inicial
        WHEN: Se llama a get_inicial
        THEN: Retorna el estado inicial
        """
        # Arrange
        estado_inicial = EstadoOrdenCompraFactory(codigo='BORRADOR', es_inicial=True)
        estado_normal = EstadoOrdenCompraFactory(codigo='APROBADA', es_inicial=False)
        repo = EstadoOrdenCompraRepository()

        # Act
        resultado = repo.get_inicial()

        # Assert
        assert resultado == estado_inicial


# ==================== TESTS DE ORDEN COMPRA REPOSITORY ====================

@pytest.mark.django_db
class TestOrdenCompraRepository:
    """Tests para OrdenCompraRepository."""

    def test_get_all_retorna_ordenes_con_relaciones_optimizadas(self):
        """
        GIVEN: Órdenes de compra
        WHEN: Se llama a get_all
        THEN: Retorna ordenes con select_related aplicado
        """
        # Arrange
        orden = OrdenCompraFactory()
        repo = OrdenCompraRepository()

        # Act
        ordenes = repo.get_all()

        # Assert
        assert orden in ordenes
        # Verificar que las relaciones están precargadas
        first_orden = ordenes[0]
        # No debería lanzar error porque select_related está aplicado
        assert first_orden.proveedor is not None
        assert first_orden.estado is not None

    def test_get_by_numero_retorna_orden_correcta(self):
        """
        GIVEN: Una orden con número específico
        WHEN: Se busca por número
        THEN: Retorna la orden correcta
        """
        # Arrange
        numero = 'OC-2025-000001'
        orden = OrdenCompraFactory(numero=numero)
        repo = OrdenCompraRepository()

        # Act
        resultado = repo.get_by_numero(numero)

        # Assert
        assert resultado == orden

    def test_filter_by_proveedor_retorna_ordenes_correctas(self):
        """
        GIVEN: Órdenes de diferentes proveedores
        WHEN: Se filtra por proveedor
        THEN: Retorna solo órdenes del proveedor especificado
        """
        # Arrange
        proveedor1 = ProveedorFactory()
        proveedor2 = ProveedorFactory()
        orden1 = OrdenCompraFactory(proveedor=proveedor1)
        orden2 = OrdenCompraFactory(proveedor=proveedor2)
        repo = OrdenCompraRepository()

        # Act
        resultados = repo.filter_by_proveedor(proveedor1)

        # Assert
        assert orden1 in resultados
        assert orden2 not in resultados

    def test_filter_by_estado_retorna_ordenes_correctas(self):
        """
        GIVEN: Órdenes en diferentes estados
        WHEN: Se filtra por estado
        THEN: Retorna solo órdenes en ese estado
        """
        # Arrange
        estado1 = EstadoOrdenCompraFactory(codigo='PENDIENTE')
        estado2 = EstadoOrdenCompraFactory(codigo='APROBADA')
        orden1 = OrdenCompraFactory(estado=estado1)
        orden2 = OrdenCompraFactory(estado=estado2)
        repo = OrdenCompraRepository()

        # Act
        resultados = repo.filter_by_estado(estado1)

        # Assert
        assert orden1 in resultados
        assert orden2 not in resultados

    def test_filter_by_solicitante_retorna_ordenes_correctas(self):
        """
        GIVEN: Órdenes de diferentes solicitantes
        WHEN: Se filtra por solicitante
        THEN: Retorna solo órdenes del solicitante especificado
        """
        # Arrange
        usuario1 = UserFactory()
        usuario2 = UserFactory()
        orden1 = OrdenCompraFactory(solicitante=usuario1)
        orden2 = OrdenCompraFactory(solicitante=usuario2)
        repo = OrdenCompraRepository()

        # Act
        resultados = repo.filter_by_solicitante(usuario1)

        # Assert
        assert orden1 in resultados
        assert orden2 not in resultados

    def test_search_busca_por_numero_y_proveedor(self):
        """
        GIVEN: Órdenes con diferentes números y proveedores
        WHEN: Se busca con un query
        THEN: Retorna órdenes que coinciden
        """
        # Arrange
        proveedor = ProveedorFactory(razon_social='Proveedor Test ABC')
        orden1 = OrdenCompraFactory(numero='OC-2025-000001', proveedor=proveedor)
        orden2 = OrdenCompraFactory(numero='OC-2025-000002')
        repo = OrdenCompraRepository()

        # Act
        resultados = repo.search('ABC')

        # Assert
        assert orden1 in resultados
        assert orden2 not in resultados


# ==================== TESTS DE RECEPCIÓN ARTÍCULO REPOSITORY ====================

@pytest.mark.django_db
class TestRecepcionArticuloRepository:
    """Tests para RecepcionArticuloRepository."""

    def test_get_all_retorna_recepciones_no_eliminadas(self):
        """
        GIVEN: Recepciones eliminadas y no eliminadas
        WHEN: Se llama a get_all
        THEN: Retorna solo recepciones no eliminadas
        """
        # Arrange
        recepcion_activa = RecepcionArticuloFactory(eliminado=False)
        recepcion_eliminada = RecepcionArticuloFactory(eliminado=True)
        repo = RecepcionArticuloRepository()

        # Act
        recepciones = repo.get_all()

        # Assert
        assert recepcion_activa in recepciones
        assert recepcion_eliminada not in recepciones

    def test_get_by_numero_retorna_recepcion_correcta(self):
        """
        GIVEN: Una recepción con número específico
        WHEN: Se busca por número
        THEN: Retorna la recepción correcta
        """
        # Arrange
        numero = 'RART-2025-000001'
        recepcion = RecepcionArticuloFactory(numero=numero)
        repo = RecepcionArticuloRepository()

        # Act
        resultado = repo.get_by_numero(numero)

        # Assert
        assert resultado == recepcion

    def test_filter_by_bodega_retorna_recepciones_correctas(self):
        """
        GIVEN: Recepciones de diferentes bodegas
        WHEN: Se filtra por bodega
        THEN: Retorna solo recepciones de esa bodega
        """
        # Arrange
        bodega1 = BodegaFactory()
        bodega2 = BodegaFactory()
        recepcion1 = RecepcionArticuloFactory(bodega=bodega1)
        recepcion2 = RecepcionArticuloFactory(bodega=bodega2)
        repo = RecepcionArticuloRepository()

        # Act
        resultados = repo.filter_by_bodega(bodega1)

        # Assert
        assert recepcion1 in resultados
        assert recepcion2 not in resultados

    def test_filter_by_estado_retorna_recepciones_correctas(self):
        """
        GIVEN: Recepciones en diferentes estados
        WHEN: Se filtra por estado
        THEN: Retorna solo recepciones en ese estado
        """
        # Arrange
        estado1 = EstadoRecepcionFactory(codigo='BORRADOR')
        estado2 = EstadoRecepcionFactory(codigo='COMPLETADA')
        recepcion1 = RecepcionArticuloFactory(estado=estado1)
        recepcion2 = RecepcionArticuloFactory(estado=estado2)
        repo = RecepcionArticuloRepository()

        # Act
        resultados = repo.filter_by_estado(estado1)

        # Assert
        assert recepcion1 in resultados
        assert recepcion2 not in resultados


# ==================== TESTS DE RECEPCIÓN ACTIVO REPOSITORY ====================

@pytest.mark.django_db
class TestRecepcionActivoRepository:
    """Tests para RecepcionActivoRepository."""

    def test_get_all_retorna_recepciones_no_eliminadas(self):
        """
        GIVEN: Recepciones de activos eliminadas y no eliminadas
        WHEN: Se llama a get_all
        THEN: Retorna solo recepciones no eliminadas
        """
        # Arrange
        recepcion_activa = RecepcionActivoFactory(eliminado=False)
        recepcion_eliminada = RecepcionActivoFactory(eliminado=True)
        repo = RecepcionActivoRepository()

        # Act
        recepciones = repo.get_all()

        # Assert
        assert recepcion_activa in recepciones
        assert recepcion_eliminada not in recepciones

    def test_get_by_id_retorna_recepcion_correcta(self):
        """
        GIVEN: Una recepción de activos con ID específico
        WHEN: Se busca por ID
        THEN: Retorna la recepción correcta
        """
        # Arrange
        recepcion = RecepcionActivoFactory()
        repo = RecepcionActivoRepository()

        # Act
        resultado = repo.get_by_id(recepcion.id)

        # Assert
        assert resultado == recepcion


# ==================== TESTS DE DETALLE RECEPCIÓN REPOSITORY ====================

@pytest.mark.django_db
class TestDetalleRecepcionArticuloRepository:
    """Tests para DetalleRecepcionArticuloRepository."""

    def test_filter_by_recepcion_retorna_detalles_correctos(self):
        """
        GIVEN: Detalles de diferentes recepciones
        WHEN: Se filtra por recepción
        THEN: Retorna solo detalles de esa recepción
        """
        # Arrange
        recepcion1 = RecepcionArticuloFactory()
        recepcion2 = RecepcionArticuloFactory()
        detalle1 = DetalleRecepcionArticuloFactory(recepcion=recepcion1, eliminado=False)
        detalle2 = DetalleRecepcionArticuloFactory(recepcion=recepcion2, eliminado=False)
        repo = DetalleRecepcionArticuloRepository()

        # Act
        resultados = repo.filter_by_recepcion(recepcion1)

        # Assert
        assert detalle1 in resultados
        assert detalle2 not in resultados

    def test_filter_by_recepcion_excluye_eliminados(self):
        """
        GIVEN: Detalles eliminados y no eliminados de una recepción
        WHEN: Se filtra por recepción
        THEN: Retorna solo detalles no eliminados
        """
        # Arrange
        recepcion = RecepcionArticuloFactory()
        detalle_activo = DetalleRecepcionArticuloFactory(recepcion=recepcion, eliminado=False)
        detalle_eliminado = DetalleRecepcionArticuloFactory(recepcion=recepcion, eliminado=True)
        repo = DetalleRecepcionArticuloRepository()

        # Act
        resultados = repo.filter_by_recepcion(recepcion)

        # Assert
        assert detalle_activo in resultados
        assert detalle_eliminado not in resultados
