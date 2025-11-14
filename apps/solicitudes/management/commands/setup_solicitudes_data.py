from django.core.management.base import BaseCommand
from apps.solicitudes.models import TipoSolicitud, EstadoSolicitud


class Command(BaseCommand):
    help = 'Inicializa datos básicos para el módulo de solicitudes (estados y tipos)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Inicializando datos de Solicitudes...'))

        # Crear Estados de Solicitud
        estados = [
            {
                'codigo': 'PENDIENTE',
                'nombre': 'Pendiente',
                'descripcion': 'Solicitud creada, pendiente de aprobación',
                'color': '#ffc107',  # Amarillo
                'es_inicial': True,
                'es_final': False,
                'requiere_accion': True,
            },
            {
                'codigo': 'APROBADA',
                'nombre': 'Aprobada',
                'descripcion': 'Solicitud aprobada, pendiente de despacho',
                'color': '#28a745',  # Verde
                'es_inicial': False,
                'es_final': False,
                'requiere_accion': True,
            },
            {
                'codigo': 'RECHAZADA',
                'nombre': 'Rechazada',
                'descripcion': 'Solicitud rechazada',
                'color': '#dc3545',  # Rojo
                'es_inicial': False,
                'es_final': True,
                'requiere_accion': False,
            },
            {
                'codigo': 'DESPACHADA',
                'nombre': 'Despachada',
                'descripcion': 'Solicitud despachada completamente',
                'color': '#17a2b8',  # Azul claro
                'es_inicial': False,
                'es_final': True,
                'requiere_accion': False,
            },
            {
                'codigo': 'CANCELADA',
                'nombre': 'Cancelada',
                'descripcion': 'Solicitud cancelada por el solicitante',
                'color': '#6c757d',  # Gris
                'es_inicial': False,
                'es_final': True,
                'requiere_accion': False,
            },
        ]

        for estado_data in estados:
            estado, created = EstadoSolicitud.objects.get_or_create(
                codigo=estado_data['codigo'],
                defaults=estado_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'  [+] Estado creado: {estado.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  [-] Estado ya existe: {estado.nombre}')
                )

        # Crear Tipos de Solicitud
        tipos = [
            {
                'codigo': 'MAT',
                'nombre': 'Solicitud de Materiales',
                'descripcion': 'Solicitud de materiales de oficina, insumos médicos u otros consumibles',
                'requiere_aprobacion': True,
            },
            {
                'codigo': 'ACT',
                'nombre': 'Solicitud de Activos',
                'descripcion': 'Solicitud de equipos, muebles u otros activos fijos',
                'requiere_aprobacion': True,
            },
            {
                'codigo': 'URG',
                'nombre': 'Solicitud Urgente',
                'descripcion': 'Solicitud urgente que requiere atención inmediata',
                'requiere_aprobacion': True,
            },
            {
                'codigo': 'MAN',
                'nombre': 'Solicitud de Mantenimiento',
                'descripcion': 'Solicitud de materiales para mantenimiento',
                'requiere_aprobacion': True,
            },
        ]

        for tipo_data in tipos:
            tipo, created = TipoSolicitud.objects.get_or_create(
                codigo=tipo_data['codigo'],
                defaults=tipo_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'  [+] Tipo creado: {tipo.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  [-] Tipo ya existe: {tipo.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS('\nDatos inicializados correctamente!')
        )
