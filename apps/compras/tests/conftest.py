"""
Configuración de fixtures y utilidades para tests de compras.
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.models import User
from apps.compras.models import (
    EstadoOrdenCompra, EstadoRecepcion, TipoRecepcion,
    Proveedor, OrdenCompra, RecepcionArticulo, RecepcionActivo
)
from apps.bodega.models import Bodega, Categoria as CategoriaBodega, Articulo
from apps.activos.models import CategoriaActivo, Activo, UnidadMedida, EstadoActivo


# ==================== FIXTURES DE USUARIOS ====================

@pytest.fixture
def usuario_test(db):
    """Crea un usuario de test."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def usuario_admin(db):
    """Crea un usuario administrador."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User'
    )


# ==================== FIXTURES DE ESTADOS ====================

@pytest.fixture
def estado_orden_pendiente(db):
    """Crea estado PENDIENTE para órdenes de compra."""
    return EstadoOrdenCompra.objects.create(
        codigo='PENDIENTE',
        nombre='Pendiente',
        descripcion='Orden pendiente de aprobación',
        color='#ffc107',
        es_inicial=True,
        es_final=False,
        permite_edicion=True,
        activo=True
    )


@pytest.fixture
def estado_orden_aprobada(db):
    """Crea estado APROBADA para órdenes de compra."""
    return EstadoOrdenCompra.objects.create(
        codigo='APROBADA',
        nombre='Aprobada',
        descripcion='Orden aprobada',
        color='#28a745',
        es_inicial=False,
        es_final=False,
        permite_edicion=True,
        activo=True
    )


@pytest.fixture
def estado_orden_finalizada(db):
    """Crea estado FINALIZADA para órdenes de compra."""
    return EstadoOrdenCompra.objects.create(
        codigo='FINALIZADA',
        nombre='Finalizada',
        descripcion='Orden completada',
        color='#6c757d',
        es_inicial=False,
        es_final=True,
        permite_edicion=False,
        activo=True
    )


@pytest.fixture
def estado_recepcion_inicial(db):
    """Crea estado inicial para recepciones."""
    return EstadoRecepcion.objects.create(
        codigo='BORRADOR',
        nombre='Borrador',
        descripcion='Recepción en borrador',
        color='#6c757d',
        es_inicial=True,
        es_final=False
    )


@pytest.fixture
def estado_recepcion_completada(db):
    """Crea estado COMPLETADA para recepciones."""
    return EstadoRecepcion.objects.create(
        codigo='COMPLETADA',
        nombre='Completada',
        descripcion='Recepción completada',
        color='#28a745',
        es_inicial=False,
        es_final=True
    )


@pytest.fixture
def tipo_recepcion_con_orden(db):
    """Crea tipo de recepción que requiere orden de compra."""
    return TipoRecepcion.objects.create(
        codigo='CON_ORDEN',
        nombre='Con Orden de Compra',
        descripcion='Recepción asociada a orden de compra',
        requiere_orden=True,
        activo=True
    )


@pytest.fixture
def tipo_recepcion_sin_orden(db):
    """Crea tipo de recepción que NO requiere orden de compra."""
    return TipoRecepcion.objects.create(
        codigo='SIN_ORDEN',
        nombre='Sin Orden de Compra',
        descripcion='Recepción directa sin orden',
        requiere_orden=False,
        activo=True
    )


# ==================== FIXTURES DE PROVEEDOR ====================

@pytest.fixture
def proveedor_activo(db):
    """Crea un proveedor activo de test."""
    return Proveedor.objects.create(
        rut='76.123.456-7',
        razon_social='Proveedor Test S.A.',
        nombre_fantasia='Proveedor Test',
        giro='Comercio',
        direccion='Av. Test 123',
        comuna='Santiago',
        ciudad='Santiago',
        telefono='+56912345678',
        email='contacto@proveedortest.cl',
        condicion_pago='30 días',
        dias_credito=30,
        activo=True,
        eliminado=False
    )


@pytest.fixture
def proveedor_inactivo(db):
    """Crea un proveedor inactivo."""
    return Proveedor.objects.create(
        rut='76.654.321-K',
        razon_social='Proveedor Inactivo S.A.',
        direccion='Calle Inactiva 456',
        activo=False,
        eliminado=False
    )


# ==================== FIXTURES DE BODEGA ====================

@pytest.fixture
def bodega_principal(db, usuario_test):
    """Crea bodega principal de test."""
    return Bodega.objects.create(
        codigo='BOD-001',
        nombre='Bodega Principal',
        descripcion='Bodega principal de test',
        responsable=usuario_test,
        activo=True,
        eliminado=False
    )


@pytest.fixture
def categoria_bodega(db):
    """Crea categoría de bodega de test."""
    return CategoriaBodega.objects.create(
        codigo='CAT-001',
        nombre='Materiales de Oficina',
        descripcion='Materiales de oficina varios',
        activo=True,
        eliminado=False
    )


@pytest.fixture
def articulo_test(db, categoria_bodega, bodega_principal):
    """Crea artículo de test para bodega."""
    return Articulo.objects.create(
        sku='ART-001',
        codigo='ART-001',
        nombre='Lápiz HB',
        descripcion='Lápiz grafito HB',
        categoria=categoria_bodega,
        unidad_medida='UNIDAD',
        ubicacion_fisica=bodega_principal,
        stock_actual=Decimal('100.00'),
        stock_minimo=Decimal('10.00'),
        stock_maximo=Decimal('500.00'),
        activo=True,
        eliminado=False
    )


# ==================== FIXTURES DE ACTIVOS ====================

@pytest.fixture
def estado_activo_disponible(db):
    """Crea estado disponible para activos."""
    return EstadoActivo.objects.create(
        codigo='DISPONIBLE',
        nombre='Disponible',
        descripcion='Activo disponible para uso',
        color='#28a745',
        es_inicial=True,
        permite_movimiento=True,
        activo=True,
        eliminado=False
    )


@pytest.fixture
def unidad_medida_unidad(db):
    """Crea unidad de medida UNIDAD."""
    return UnidadMedida.objects.create(
        codigo='UNIDAD',
        nombre='Unidad',
        simbolo='UND',
        activo=True,
        eliminado=False
    )


@pytest.fixture
def categoria_activo(db):
    """Crea categoría de activo de test."""
    return CategoriaActivo.objects.create(
        codigo='ACT-001',
        nombre='Equipamiento Informático',
        descripcion='Equipos informáticos varios',
        activo=True,
        eliminado=False
    )


@pytest.fixture
def activo_test(db, categoria_activo, unidad_medida_unidad, estado_activo_disponible):
    """Crea activo de test."""
    return Activo.objects.create(
        codigo='ACT-001',
        nombre='Notebook HP',
        descripcion='Notebook HP 15 pulgadas',
        categoria=categoria_activo,
        unidad_medida=unidad_medida_unidad,
        estado=estado_activo_disponible,
        requiere_serie=True,
        activo=True,
        eliminado=False
    )


@pytest.fixture
def activo_sin_serie(db, categoria_activo, unidad_medida_unidad, estado_activo_disponible):
    """Crea activo que NO requiere serie."""
    return Activo.objects.create(
        codigo='ACT-002',
        nombre='Silla de Oficina',
        descripcion='Silla ergonómica de oficina',
        categoria=categoria_activo,
        unidad_medida=unidad_medida_unidad,
        estado=estado_activo_disponible,
        requiere_serie=False,
        activo=True,
        eliminado=False
    )


# ==================== FIXTURES DE ORDEN DE COMPRA ====================

@pytest.fixture
def orden_compra_test(db, proveedor_activo, bodega_principal, estado_orden_pendiente, usuario_test):
    """Crea orden de compra de test."""
    return OrdenCompra.objects.create(
        numero='OC-2025-000001',
        fecha_orden=date.today(),
        fecha_entrega_esperada=date.today() + timedelta(days=7),
        proveedor=proveedor_activo,
        bodega_destino=bodega_principal,
        estado=estado_orden_pendiente,
        solicitante=usuario_test,
        subtotal=Decimal('10000.00'),
        impuesto=Decimal('1900.00'),
        descuento=Decimal('0.00'),
        total=Decimal('11900.00'),
        observaciones='Orden de compra de test'
    )


# ==================== FIXTURES DE RECEPCIÓN ====================

@pytest.fixture
def recepcion_articulo_test(
    db,
    bodega_principal,
    estado_recepcion_inicial,
    usuario_test,
    orden_compra_test,
    tipo_recepcion_con_orden
):
    """Crea recepción de artículos de test."""
    return RecepcionArticulo.objects.create(
        numero='RART-2025-000001',
        bodega=bodega_principal,
        estado=estado_recepcion_inicial,
        recibido_por=usuario_test,
        orden_compra=orden_compra_test,
        tipo=tipo_recepcion_con_orden,
        documento_referencia='GUIA-12345',
        observaciones='Recepción de test'
    )


@pytest.fixture
def recepcion_activo_test(
    db,
    estado_recepcion_inicial,
    usuario_test,
    orden_compra_test,
    tipo_recepcion_con_orden
):
    """Crea recepción de activos de test."""
    return RecepcionActivo.objects.create(
        numero='RACT-2025-000001',
        estado=estado_recepcion_inicial,
        recibido_por=usuario_test,
        orden_compra=orden_compra_test,
        tipo=tipo_recepcion_con_orden,
        documento_referencia='GUIA-67890',
        observaciones='Recepción de activos de test'
    )


# ==================== FIXTURES DE ESTADOS COMPLETOS ====================

@pytest.fixture
def estados_orden_completos(db):
    """Crea todos los estados de orden de compra necesarios."""
    estados = {
        'pendiente': EstadoOrdenCompra.objects.create(
            codigo='PENDIENTE',
            nombre='Pendiente',
            es_inicial=True,
            es_final=False,
            permite_edicion=True,
            activo=True
        ),
        'aprobada': EstadoOrdenCompra.objects.create(
            codigo='APROBADA',
            nombre='Aprobada',
            es_inicial=False,
            es_final=False,
            permite_edicion=True,
            activo=True
        ),
        'finalizada': EstadoOrdenCompra.objects.create(
            codigo='FINALIZADA',
            nombre='Finalizada',
            es_inicial=False,
            es_final=True,
            permite_edicion=False,
            activo=True
        ),
    }
    return estados


@pytest.fixture
def estados_recepcion_completos(db):
    """Crea todos los estados de recepción necesarios."""
    estados = {
        'borrador': EstadoRecepcion.objects.create(
            codigo='BORRADOR',
            nombre='Borrador',
            es_inicial=True,
            es_final=False
        ),
        'completada': EstadoRecepcion.objects.create(
            codigo='COMPLETADA',
            nombre='Completada',
            es_inicial=False,
            es_final=True
        ),
    }
    return estados
