from django.core.management.base import BaseCommand
from apps.activos.models import Ubicacion, TipoMovimientoActivo, EstadoActivo


class Command(BaseCommand):
    help = 'Inicializa datos básicos para el módulo de activos: ubicaciones, tipos de movimiento y estados'

    def handle(self, *args, **options):
        self.stdout.write('[+] Iniciando configuración de datos básicos de activos...\n')

        # Crear ubicaciones
        self.stdout.write('\n[+] Creando ubicaciones...')
        ubicaciones_data = [
            {
                'codigo': 'OFI-001',
                'nombre': 'Oficina Principal',
                'descripcion': 'Oficina administrativa principal',
                'edificio': 'Edificio Central',
                'piso': 'Piso 1',
                'area': 'Administración'
            },
            {
                'codigo': 'BOD-001',
                'nombre': 'Bodega General',
                'descripcion': 'Bodega principal de almacenamiento',
                'edificio': 'Edificio Central',
                'piso': 'Sótano',
                'area': 'Bodega'
            },
            {
                'codigo': 'LAB-001',
                'nombre': 'Laboratorio de Cómputo',
                'descripcion': 'Laboratorio de computación',
                'edificio': 'Edificio Académico',
                'piso': 'Piso 2',
                'area': 'Educación'
            },
            {
                'codigo': 'MAN-001',
                'nombre': 'Área de Mantenimiento',
                'descripcion': 'Taller de mantenimiento y reparaciones',
                'edificio': 'Edificio de Servicios',
                'piso': 'Planta Baja',
                'area': 'Mantenimiento'
            },
        ]

        ubicaciones_creadas = 0
        for data in ubicaciones_data:
            obj, created = Ubicacion.objects.get_or_create(
                codigo=data['codigo'],
                defaults=data
            )
            if created:
                ubicaciones_creadas += 1
                self.stdout.write(f'  [+] {data["nombre"]}')

        self.stdout.write(f'\n[+] Ubicaciones creadas: {ubicaciones_creadas}/{len(ubicaciones_data)}')

        # Crear tipos de movimiento
        self.stdout.write('\n[+] Creando tipos de movimiento...')
        tipos_movimiento_data = [
            {
                'codigo': 'ASIG',
                'nombre': 'Asignación',
                'descripcion': 'Asignación de activo a usuario o ubicación',
                'requiere_ubicacion': True,
                'requiere_responsable': True
            },
            {
                'codigo': 'TRASL',
                'nombre': 'Traslado',
                'descripcion': 'Traslado de activo entre ubicaciones',
                'requiere_ubicacion': True,
                'requiere_responsable': False
            },
            {
                'codigo': 'MANT',
                'nombre': 'Mantenimiento',
                'descripcion': 'Envío de activo a mantenimiento',
                'requiere_ubicacion': True,
                'requiere_responsable': False
            },
            {
                'codigo': 'BAJA',
                'nombre': 'Baja',
                'descripcion': 'Baja de activo del inventario',
                'requiere_ubicacion': False,
                'requiere_responsable': False
            },
            {
                'codigo': 'DEV',
                'nombre': 'Devolución',
                'descripcion': 'Devolución de activo asignado',
                'requiere_ubicacion': True,
                'requiere_responsable': False
            },
        ]

        tipos_creados = 0
        for data in tipos_movimiento_data:
            obj, created = TipoMovimientoActivo.objects.get_or_create(
                codigo=data['codigo'],
                defaults=data
            )
            if created:
                tipos_creados += 1
                self.stdout.write(f'  [+] {data["nombre"]}')

        self.stdout.write(f'\n[+] Tipos de movimiento creados: {tipos_creados}/{len(tipos_movimiento_data)}')

        # Crear estados de activos
        self.stdout.write('\n[+] Creando estados de activos...')
        estados_data = [
            {
                'codigo': 'NUEVO',
                'nombre': 'Nuevo',
                'descripcion': 'Activo nuevo sin uso',
                'color': '#28a745',  # Verde
                'es_inicial': True,
                'permite_movimiento': True
            },
            {
                'codigo': 'BUENO',
                'nombre': 'Buen Estado',
                'descripcion': 'Activo en buen estado de funcionamiento',
                'color': '#17a2b8',  # Azul claro
                'es_inicial': False,
                'permite_movimiento': True
            },
            {
                'codigo': 'REGULAR',
                'nombre': 'Estado Regular',
                'descripcion': 'Activo con desgaste normal',
                'color': '#ffc107',  # Amarillo
                'es_inicial': False,
                'permite_movimiento': True
            },
            {
                'codigo': 'MANT',
                'nombre': 'En Mantenimiento',
                'descripcion': 'Activo en proceso de mantenimiento o reparación',
                'color': '#fd7e14',  # Naranja
                'es_inicial': False,
                'permite_movimiento': False
            },
            {
                'codigo': 'DAÑADO',
                'nombre': 'Dañado',
                'descripcion': 'Activo dañado no funcional',
                'color': '#dc3545',  # Rojo
                'es_inicial': False,
                'permite_movimiento': False
            },
            {
                'codigo': 'BAJA',
                'nombre': 'Dado de Baja',
                'descripcion': 'Activo dado de baja del inventario',
                'color': '#6c757d',  # Gris
                'es_inicial': False,
                'permite_movimiento': False
            },
        ]

        estados_creados = 0
        for data in estados_data:
            obj, created = EstadoActivo.objects.get_or_create(
                codigo=data['codigo'],
                defaults=data
            )
            if created:
                estados_creados += 1
                self.stdout.write(f'  [+] {data["nombre"]} - {data["color"]}')

        self.stdout.write(f'\n[+] Estados creados: {estados_creados}/{len(estados_data)}')

        # Resumen final
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('\nConfiguración completada exitosamente!'))
        self.stdout.write('\nResumen:')
        self.stdout.write(f'  - Ubicaciones: {ubicaciones_creadas} nuevas')
        self.stdout.write(f'  - Tipos de movimiento: {tipos_creados} nuevos')
        self.stdout.write(f'  - Estados de activos: {estados_creados} nuevos')
        self.stdout.write('\n' + '=' * 60 + '\n')
