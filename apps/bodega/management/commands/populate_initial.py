from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import datetime


class Command(BaseCommand):
    help = 'Populate initial catalog data for bodega, activos, compras and solicitudes safely'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Create admin user if not exists
        admin, created = User.objects.get_or_create(username='admin', defaults={
            'is_superuser': True,
            'is_staff': True,
            'email': 'admin@example.com'
        })
        if created:
            admin.set_password('admin')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (username=admin, password=admin)'))
        else:
            self.stdout.write('Admin user already exists')

        # Helper to set fields only if present on model
        def safe_get_or_create(model, data_list):
            for data in data_list:
                kwargs = {}
                for key, val in data.items():
                    field = None
                    # support keys provided as fk_id or fk
                    if key.endswith('_id'):
                        base_key = key[:-3]
                        try:
                            field = model._meta.get_field(base_key)
                        except Exception:
                            # fallback to field named exactly as provided
                            try:
                                field = model._meta.get_field(key)
                            except Exception:
                                field = None
                    else:
                        try:
                            field = model._meta.get_field(key)
                        except Exception:
                            # try id variant
                            try:
                                field = model._meta.get_field(key + '_id')
                            except Exception:
                                field = None

                    if field is None:
                        # unknown field for this model, skip
                        continue

                    # If FK, set the <field_name>_id when value is an int
                    if hasattr(field, 'remote_field') and field.remote_field is not None:
                        fk_field_name = field.name
                        if isinstance(val, int):
                            kwargs[f"{fk_field_name}_id"] = val
                        else:
                            kwargs[fk_field_name] = val
                        continue

                    # parse datetimes for DateTimeField-like types
                    try:
                        internal_type = field.get_internal_type()
                    except Exception:
                        internal_type = ''

                    if internal_type == 'DateTimeField' and isinstance(val, str):
                        parsed = parse_datetime(val)
                        kwargs[field.name] = parsed or val
                    else:
                        kwargs[field.name] = val

                obj, created = (model.objects.update_or_create(pk=data.get('pk'), defaults=kwargs)
                                if data.get('pk') else model.objects.get_or_create(**kwargs))
                self.stdout.write(self.style.SUCCESS(f"Set {model.__name__}: {getattr(obj, 'pk', obj)}"))

        # Import models
        try:
            from apps.bodega.models import Categoria, Articulo, UnidadMedida, TipoEntrega, Bodega
            from apps.activos.models import CategoriaActivo, Activo, Marca, Ubicacion, Taller, EstadoActivo
            from apps.compras.models import Proveedor, TipoRecepcion, EstadoRecepcion, EstadoOrdenCompra
            from apps.solicitudes.models import Departamento, TipoSolicitud, EstadoSolicitud
        except Exception as e:
            self.stderr.write(f"Error importing models: {e}")
            return

        now = timezone.make_aware(datetime.datetime(2020, 1, 1, 0, 0, 0), timezone.get_current_timezone())

        safe_get_or_create(Bodega, [
            {'pk': 1, 'codigo': 'BOD01', 'nombre': 'Bodega Central', 'descripcion': 'Bodega principal', 'responsable': admin.pk, 'activo': True, 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(UnidadMedida, [
            {'pk': 1, 'codigo': 'UND', 'nombre': 'Unidad', 'simbolo': 'u', 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 2, 'codigo': 'KG', 'nombre': 'Kilogramo', 'simbolo': 'kg', 'fecha_creacion': now, 'fecha_actualizacion': now},
        ])

        safe_get_or_create(Categoria, [
            {'pk': 1, 'codigo': 'MAT', 'nombre': 'Materiales', 'descripcion': 'Materiales de oficina', 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(CategoriaActivo, [
            {'pk': 1, 'codigo': 'EQ', 'nombre': 'Equipos', 'descripcion': 'Equipos y mobiliario', 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(EstadoActivo, [
            {'pk': 1, 'codigo': 'DISP', 'nombre': 'Disponible', 'descripcion': 'Disponible', 'color': '#28a745', 'es_inicial': True, 'permite_movimiento': True, 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(Marca, [
            {'pk': 1, 'codigo': 'MAR01', 'nombre': 'Marca Ejemplo', 'descripcion': 'Marca genérica', 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(Ubicacion, [
            {'pk': 1, 'codigo': 'UB01', 'nombre': 'Almacén Central', 'descripcion': 'Ubicación principal', 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(Taller, [
            {'pk': 1, 'codigo': 'TAL01', 'nombre': 'Taller Central', 'descripcion': 'Taller mantenimiento', 'ubicacion': 'Edificio A - Sótano', 'responsable': admin.pk, 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(Proveedor, [
            {'pk': 1, 'rut': '12345678-9', 'razon_social': 'Proveedor Ejemplo SA', 'direccion': 'Calle Falsa 123', 'telefono': '+56912345678', 'email': 'proveedor@example.com', 'sitio_web': 'https://proveedor.example.com', 'activo': True, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(TipoRecepcion, [
            {'pk': 1, 'codigo': 'COMPRA', 'nombre': 'Recepción por Compra', 'descripcion': 'Recepción por compra', 'requiere_orden': True, 'activo': True, 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(TipoEntrega, [
            {'pk': 1, 'codigo': 'DESPACHO', 'nombre': 'Despacho Interno', 'descripcion': 'Entrega interna', 'requiere_autorizacion': False, 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        # Estados y tipos relacionados con compras (recepciones y órdenes)
        safe_get_or_create(EstadoRecepcion, [
            {'pk': 1, 'codigo': 'PENDIENTE', 'nombre': 'Pendiente', 'descripcion': 'Recepción pendiente', 'color': '#ffc107', 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 2, 'codigo': 'COMPLETADA', 'nombre': 'Completada', 'descripcion': 'Recepción completada', 'color': '#28a745', 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 3, 'codigo': 'CANCELADA', 'nombre': 'Cancelada', 'descripcion': 'Recepción cancelada', 'color': '#dc3545', 'fecha_creacion': now, 'fecha_actualizacion': now},
        ])

        safe_get_or_create(EstadoOrdenCompra, [
            {'pk': 1, 'codigo': 'PENDIENTE', 'nombre': 'Pendiente', 'descripcion': 'Orden pendiente', 'color': '#ffc107', 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 2, 'codigo': 'APROBADA', 'nombre': 'Aprobada', 'descripcion': 'Orden aprobada', 'color': '#28a745', 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 3, 'codigo': 'RECIBIDA', 'nombre': 'Recibida', 'descripcion': 'Orden recibida', 'color': '#007bff', 'fecha_creacion': now, 'fecha_actualizacion': now},
        ])

        safe_get_or_create(Articulo, [
            {'pk': 1, 'codigo': 'ART-001', 'nombre': 'Papel A4 500 hojas', 'descripcion': 'Resma de papel A4', 'categoria_id': 1, 'stock_actual': 100, 'stock_minimo': 10, 'stock_maximo': 500, 'punto_reorden': 20, 'ubicacion_fisica_id': 1, 'observaciones': 'Artículo inicial', 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        # Tipos y estados para solicitudes
        safe_get_or_create(TipoSolicitud, [
            {'pk': 1, 'codigo': 'NORMAL', 'nombre': 'Solicitud Normal', 'descripcion': 'Solicitud estándar', 'requiere_aprobacion': True, 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 2, 'codigo': 'URGENTE', 'nombre': 'Solicitud Urgente', 'descripcion': 'Solicitud con prioridad alta', 'requiere_aprobacion': True, 'fecha_creacion': now, 'fecha_actualizacion': now},
        ])

        safe_get_or_create(EstadoSolicitud, [
            {'pk': 1, 'codigo': 'BORRADOR', 'nombre': 'Borrador', 'descripcion': 'Solicitudes en borrador', 'color': '#6c757d', 'es_inicial': True, 'es_final': False, 'requiere_accion': False, 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 2, 'codigo': 'EN_APROBACION', 'nombre': 'En Aprobación', 'descripcion': 'Solicitudes en proceso de aprobación', 'color': '#ffc107', 'es_inicial': False, 'es_final': False, 'requiere_accion': True, 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 3, 'codigo': 'APROBADA', 'nombre': 'Aprobada', 'descripcion': 'Solicitud aprobada', 'color': '#28a745', 'es_inicial': False, 'es_final': False, 'requiere_accion': False, 'fecha_creacion': now, 'fecha_actualizacion': now},
            {'pk': 4, 'codigo': 'DESPACHADA', 'nombre': 'Despachada', 'descripcion': 'Solicitud despachada', 'color': '#007bff', 'es_inicial': False, 'es_final': True, 'requiere_accion': False, 'fecha_creacion': now, 'fecha_actualizacion': now},
        ])

        safe_get_or_create(Activo, [
            {'pk': 1, 'codigo': 'ACT-001', 'nombre': 'Laptop Dell Inspiron', 'descripcion': 'Laptop para oficina', 'categoria_id': 1, 'estado_id': 1, 'marca_id': 1, 'numero_serie': 'SN123456', 'precio_unitario': '450000.00', 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        safe_get_or_create(Departamento, [
            {'pk': 1, 'codigo': 'DEP01', 'nombre': 'Dirección', 'descripcion': 'Departamento de Dirección', 'responsable': None, 'activo': True, 'fecha_creacion': now, 'fecha_actualizacion': now}
        ])

        self.stdout.write(self.style.SUCCESS('Initial population completed.'))
