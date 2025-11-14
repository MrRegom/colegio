"""
Factories para modelos de compras usando factory_boy.
Facilita la creación de datos de test de forma declarativa y reproducible.
"""
import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.models import User
from apps.compras.models import (
    Proveedor, EstadoOrdenCompra, OrdenCompra,
    DetalleOrdenCompra, DetalleOrdenCompraArticulo,
    EstadoRecepcion, TipoRecepcion,
    RecepcionArticulo, DetalleRecepcionArticulo,
    RecepcionActivo, DetalleRecepcionActivo
)
from apps.bodega.models import Bodega, Categoria as CategoriaBodega, Articulo
from apps.activos.models import CategoriaActivo, Activo, UnidadMedida, EstadoActivo


# ==================== FACTORIES DE USUARIOS ====================

class UserFactory(DjangoModelFactory):
    """Factory para User."""
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


# ==================== FACTORIES DE ESTADOS ====================

class EstadoOrdenCompraFactory(DjangoModelFactory):
    """Factory para EstadoOrdenCompra."""
    class Meta:
        model = EstadoOrdenCompra
        django_get_or_create = ('codigo',)

    codigo = factory.Sequence(lambda n: f'ESTADO-{n}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    color = '#6c757d'
    es_inicial = False
    es_final = False
    permite_edicion = True
    activo = True


class EstadoRecepcionFactory(DjangoModelFactory):
    """Factory para EstadoRecepcion."""
    class Meta:
        model = EstadoRecepcion
        django_get_or_create = ('codigo',)

    codigo = factory.Sequence(lambda n: f'ESTADO-REC-{n}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    color = '#6c757d'
    es_inicial = False
    es_final = False


class TipoRecepcionFactory(DjangoModelFactory):
    """Factory para TipoRecepcion."""
    class Meta:
        model = TipoRecepcion
        django_get_or_create = ('codigo',)

    codigo = factory.Sequence(lambda n: f'TIPO-{n}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    requiere_orden = False
    activo = True


# ==================== FACTORIES DE PROVEEDOR ====================

class ProveedorFactory(DjangoModelFactory):
    """Factory para Proveedor."""
    class Meta:
        model = Proveedor

    rut = factory.Sequence(lambda n: f'76.{1234567 + n:07d}-{(n % 10)}')
    razon_social = factory.Faker('company')
    nombre_fantasia = factory.Faker('company')
    giro = factory.Faker('bs')
    direccion = factory.Faker('address')
    comuna = factory.Faker('city')
    ciudad = factory.Faker('city')
    telefono = factory.Faker('phone_number')
    email = factory.Faker('company_email')
    condicion_pago = fuzzy.FuzzyChoice(['Contado', '30 días', '60 días', '90 días'])
    dias_credito = fuzzy.FuzzyInteger(0, 90)
    activo = True
    eliminado = False


# ==================== FACTORIES DE BODEGA ====================

class BodegaFactory(DjangoModelFactory):
    """Factory para Bodega."""
    class Meta:
        model = Bodega

    codigo = factory.Sequence(lambda n: f'BOD-{n:03d}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    responsable = factory.SubFactory(UserFactory)
    activo = True
    eliminado = False


class CategoriaBodegaFactory(DjangoModelFactory):
    """Factory para Categoria de Bodega."""
    class Meta:
        model = CategoriaBodega

    codigo = factory.Sequence(lambda n: f'CAT-{n:03d}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    activo = True
    eliminado = False


class ArticuloFactory(DjangoModelFactory):
    """Factory para Articulo."""
    class Meta:
        model = Articulo

    sku = factory.Sequence(lambda n: f'ART-{n:06d}')
    codigo = factory.LazyAttribute(lambda obj: obj.sku)
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    categoria = factory.SubFactory(CategoriaBodegaFactory)
    unidad_medida = fuzzy.FuzzyChoice(['UNIDAD', 'KILOGRAMO', 'METRO', 'LITRO'])
    ubicacion_fisica = factory.SubFactory(BodegaFactory)
    stock_actual = fuzzy.FuzzyDecimal(0, 1000, 2)
    stock_minimo = fuzzy.FuzzyDecimal(5, 50, 2)
    stock_maximo = fuzzy.FuzzyDecimal(500, 2000, 2)
    activo = True
    eliminado = False


# ==================== FACTORIES DE ACTIVOS ====================

class EstadoActivoFactory(DjangoModelFactory):
    """Factory para EstadoActivo."""
    class Meta:
        model = EstadoActivo
        django_get_or_create = ('codigo',)

    codigo = factory.Sequence(lambda n: f'EST-ACT-{n}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    color = '#6c757d'
    es_inicial = False
    permite_movimiento = True
    activo = True
    eliminado = False


class UnidadMedidaFactory(DjangoModelFactory):
    """Factory para UnidadMedida."""
    class Meta:
        model = UnidadMedida
        django_get_or_create = ('codigo',)

    codigo = factory.Sequence(lambda n: f'UND-{n}')
    nombre = factory.Faker('word')
    simbolo = factory.LazyAttribute(lambda obj: obj.codigo[:3].upper())
    activo = True
    eliminado = False


class CategoriaActivoFactory(DjangoModelFactory):
    """Factory para Categoria de Activo."""
    class Meta:
        model = CategoriaActivo

    codigo = factory.Sequence(lambda n: f'ACT-CAT-{n:03d}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    activo = True
    eliminado = False


class ActivoFactory(DjangoModelFactory):
    """Factory para Activo."""
    class Meta:
        model = Activo

    codigo = factory.Sequence(lambda n: f'ACT-{n:06d}')
    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')
    categoria = factory.SubFactory(CategoriaActivoFactory)
    unidad_medida = factory.SubFactory(UnidadMedidaFactory)
    estado = factory.SubFactory(EstadoActivoFactory)
    requiere_serie = fuzzy.FuzzyChoice([True, False])
    activo = True
    eliminado = False


# ==================== FACTORIES DE ORDEN DE COMPRA ====================

class OrdenCompraFactory(DjangoModelFactory):
    """Factory para OrdenCompra."""
    class Meta:
        model = OrdenCompra

    numero = factory.Sequence(lambda n: f'OC-2025-{n:06d}')
    fecha_orden = factory.LazyFunction(date.today)
    fecha_entrega_esperada = factory.LazyAttribute(
        lambda obj: obj.fecha_orden + timedelta(days=7)
    )
    proveedor = factory.SubFactory(ProveedorFactory)
    bodega_destino = factory.SubFactory(BodegaFactory)
    estado = factory.SubFactory(EstadoOrdenCompraFactory)
    solicitante = factory.SubFactory(UserFactory)
    aprobador = None
    subtotal = fuzzy.FuzzyDecimal(1000, 100000, 2)
    impuesto = factory.LazyAttribute(lambda obj: obj.subtotal * Decimal('0.19'))
    descuento = Decimal('0.00')
    total = factory.LazyAttribute(lambda obj: obj.subtotal + obj.impuesto - obj.descuento)
    observaciones = factory.Faker('sentence')
    notas_internas = factory.Faker('sentence')


class DetalleOrdenCompraArticuloFactory(DjangoModelFactory):
    """Factory para DetalleOrdenCompraArticulo."""
    class Meta:
        model = DetalleOrdenCompraArticulo

    orden_compra = factory.SubFactory(OrdenCompraFactory)
    articulo = factory.SubFactory(ArticuloFactory)
    cantidad = fuzzy.FuzzyDecimal(1, 100, 2)
    precio_unitario = fuzzy.FuzzyDecimal(100, 10000, 2)
    descuento = Decimal('0.00')
    subtotal = factory.LazyAttribute(
        lambda obj: (obj.cantidad * obj.precio_unitario) - obj.descuento
    )
    cantidad_recibida = Decimal('0.00')
    observaciones = factory.Faker('sentence')


class DetalleOrdenCompraActivoFactory(DjangoModelFactory):
    """Factory para DetalleOrdenCompra (Activos)."""
    class Meta:
        model = DetalleOrdenCompra

    orden_compra = factory.SubFactory(OrdenCompraFactory)
    activo = factory.SubFactory(ActivoFactory)
    cantidad = fuzzy.FuzzyDecimal(1, 20, 2)
    precio_unitario = fuzzy.FuzzyDecimal(10000, 500000, 2)
    descuento = Decimal('0.00')
    subtotal = factory.LazyAttribute(
        lambda obj: (obj.cantidad * obj.precio_unitario) - obj.descuento
    )
    cantidad_recibida = Decimal('0.00')
    observaciones = factory.Faker('sentence')


# ==================== FACTORIES DE RECEPCIÓN ====================

class RecepcionArticuloFactory(DjangoModelFactory):
    """Factory para RecepcionArticulo."""
    class Meta:
        model = RecepcionArticulo

    numero = factory.Sequence(lambda n: f'RART-2025-{n:06d}')
    bodega = factory.SubFactory(BodegaFactory)
    estado = factory.SubFactory(EstadoRecepcionFactory)
    recibido_por = factory.SubFactory(UserFactory)
    orden_compra = factory.SubFactory(OrdenCompraFactory)
    tipo = factory.SubFactory(TipoRecepcionFactory)
    documento_referencia = factory.Sequence(lambda n: f'GUIA-{n:05d}')
    observaciones = factory.Faker('sentence')


class DetalleRecepcionArticuloFactory(DjangoModelFactory):
    """Factory para DetalleRecepcionArticulo."""
    class Meta:
        model = DetalleRecepcionArticulo

    recepcion = factory.SubFactory(RecepcionArticuloFactory)
    articulo = factory.SubFactory(ArticuloFactory)
    cantidad = fuzzy.FuzzyDecimal(1, 100, 2)
    lote = factory.Sequence(lambda n: f'LOTE-{n:05d}')
    fecha_vencimiento = factory.LazyFunction(
        lambda: date.today() + timedelta(days=365)
    )
    observaciones = factory.Faker('sentence')


class RecepcionActivoFactory(DjangoModelFactory):
    """Factory para RecepcionActivo."""
    class Meta:
        model = RecepcionActivo

    numero = factory.Sequence(lambda n: f'RACT-2025-{n:06d}')
    estado = factory.SubFactory(EstadoRecepcionFactory)
    recibido_por = factory.SubFactory(UserFactory)
    orden_compra = factory.SubFactory(OrdenCompraFactory)
    tipo = factory.SubFactory(TipoRecepcionFactory)
    documento_referencia = factory.Sequence(lambda n: f'GUIA-ACT-{n:05d}')
    observaciones = factory.Faker('sentence')


class DetalleRecepcionActivoFactory(DjangoModelFactory):
    """Factory para DetalleRecepcionActivo."""
    class Meta:
        model = DetalleRecepcionActivo

    recepcion = factory.SubFactory(RecepcionActivoFactory)
    activo = factory.SubFactory(ActivoFactory)
    cantidad = fuzzy.FuzzyDecimal(1, 20, 2)
    numero_serie = factory.Sequence(lambda n: f'SN-{n:010d}')
    observaciones = factory.Faker('sentence')
