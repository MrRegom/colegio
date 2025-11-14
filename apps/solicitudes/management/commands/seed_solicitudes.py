# -*- coding: utf-8 -*-
# Comando de Django para poblar datos iniciales del modulo de solicitudes.
# Ejecutar con: python manage.py seed_solicitudes

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
from apps.solicitudes.models import (
    Departamento, Area, Equipo, TipoSolicitud, EstadoSolicitud
)
from apps.activos.models import (
    Activo, CategoriaActivo, UnidadMedida, EstadoActivo
)
from apps.bodega.models import Bodega


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para solicitudes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina los datos existentes antes de poblar',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            Equipo.objects.all().delete()
            Area.objects.all().delete()
            Departamento.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Datos eliminados.'))

        # Obtener o crear usuario para responsables
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                user = User.objects.create_user(
                    username='admin',
                    email='admin@example.com',
                    password='admin123',
                    is_superuser=True,
                    is_staff=True
                )
                self.stdout.write(self.style.SUCCESS(f'Usuario admin creado'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Usando usuario existente'))
            user = User.objects.first()

        # ====================== DEPARTAMENTOS ======================
        self.stdout.write(self.style.MIGRATE_HEADING('\n1. Creando Departamentos...'))
        departamentos_data = [
            {
                'codigo': 'TI',
                'nombre': 'Tecnologia e Informatica',
                'descripcion': 'Departamento encargado de la infraestructura tecnologica'
            },
            {
                'codigo': 'ADMIN',
                'nombre': 'Administracion',
                'descripcion': 'Departamento administrativo y financiero'
            },
            {
                'codigo': 'ACAD',
                'nombre': 'Academico',
                'descripcion': 'Departamento academico y de docencia'
            },
            {
                'codigo': 'MANT',
                'nombre': 'Mantenimiento',
                'descripcion': 'Departamento de mantenimiento y servicios generales'
            },
            {
                'codigo': 'RRHH',
                'nombre': 'Recursos Humanos',
                'descripcion': 'Departamento de gestion del talento humano'
            },
        ]

        departamentos = {}
        for data in departamentos_data:
            dept, created = Departamento.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'responsable': user,
                    'activo': True
                }
            )
            departamentos[data['codigo']] = dept
            status = 'Creado' if created else 'Ya existe'
            self.stdout.write(f'  - {status}: {dept.nombre}')

        # ====================== AREAS ======================
        self.stdout.write(self.style.MIGRATE_HEADING('\n2. Creando Areas...'))
        areas_data = [
            # TI
            {'codigo': 'TI-DEV', 'nombre': 'Desarrollo de Software', 'departamento': 'TI'},
            {'codigo': 'TI-INFRA', 'nombre': 'Infraestructura y Redes', 'departamento': 'TI'},
            {'codigo': 'TI-SOPOR', 'nombre': 'Soporte Tecnico', 'departamento': 'TI'},
            # ADMIN
            {'codigo': 'ADM-CONT', 'nombre': 'Contabilidad', 'departamento': 'ADMIN'},
            {'codigo': 'ADM-COMP', 'nombre': 'Compras', 'departamento': 'ADMIN'},
            {'codigo': 'ADM-FIN', 'nombre': 'Finanzas', 'departamento': 'ADMIN'},
            # ACAD
            {'codigo': 'ACAD-PRIM', 'nombre': 'Primaria', 'departamento': 'ACAD'},
            {'codigo': 'ACAD-SEC', 'nombre': 'Secundaria', 'departamento': 'ACAD'},
            {'codigo': 'ACAD-BIBLIO', 'nombre': 'Biblioteca', 'departamento': 'ACAD'},
            # MANT
            {'codigo': 'MANT-EDIF', 'nombre': 'Edificaciones', 'departamento': 'MANT'},
            {'codigo': 'MANT-JARD', 'nombre': 'Jardineria', 'departamento': 'MANT'},
            # RRHH
            {'codigo': 'RRHH-SEL', 'nombre': 'Seleccion', 'departamento': 'RRHH'},
            {'codigo': 'RRHH-CAP', 'nombre': 'Capacitacion', 'departamento': 'RRHH'},
        ]

        areas = {}
        for data in areas_data:
            area, created = Area.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'departamento': departamentos[data['departamento']],
                    'responsable': user,
                    'activo': True
                }
            )
            areas[data['codigo']] = area
            status = 'Creada' if created else 'Ya existe'
            self.stdout.write(f'  - {status}: {area.nombre} ({area.departamento.nombre})')

        # ====================== EQUIPOS ======================
        self.stdout.write(self.style.MIGRATE_HEADING('\n3. Creando Equipos...'))
        equipos_data = [
            {'codigo': 'TI-DEV-WEB', 'nombre': 'Equipo Web', 'departamento': 'TI'},
            {'codigo': 'TI-DEV-MOV', 'nombre': 'Equipo Movil', 'departamento': 'TI'},
            {'codigo': 'TI-INFRA-RED', 'nombre': 'Equipo de Redes', 'departamento': 'TI'},
            {'codigo': 'ACAD-PRIM-1', 'nombre': 'Equipo 1 a 3 Primaria', 'departamento': 'ACAD'},
            {'codigo': 'ACAD-PRIM-2', 'nombre': 'Equipo 4 a 6 Primaria', 'departamento': 'ACAD'},
            {'codigo': 'ACAD-SEC-1', 'nombre': 'Equipo 7 a 9 Secundaria', 'departamento': 'ACAD'},
            {'codigo': 'MANT-EDIF-1', 'nombre': 'Equipo Edificio Principal', 'departamento': 'MANT'},
            {'codigo': 'MANT-EDIF-2', 'nombre': 'Equipo Edificio Deportivo', 'departamento': 'MANT'},
        ]

        for data in equipos_data:
            equipo, created = Equipo.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'departamento': departamentos[data['departamento']],
                    'lider': user,
                    'activo': True
                }
            )
            status = 'Creado' if created else 'Ya existe'
            self.stdout.write(f'  - {status}: {equipo.nombre} ({equipo.departamento.nombre})')

        # ====================== UNIDADES DE MEDIDA ======================
        self.stdout.write(self.style.MIGRATE_HEADING('\n4. Creando Unidades de Medida...'))
        unidades_data = [
            {'codigo': 'UND', 'nombre': 'Unidad', 'simbolo': 'und'},
            {'codigo': 'KG', 'nombre': 'Kilogramo', 'simbolo': 'kg'},
            {'codigo': 'LT', 'nombre': 'Litro', 'simbolo': 'lt'},
            {'codigo': 'MT', 'nombre': 'Metro', 'simbolo': 'm'},
            {'codigo': 'CJA', 'nombre': 'Caja', 'simbolo': 'cja'},
            {'codigo': 'PAQ', 'nombre': 'Paquete', 'simbolo': 'paq'},
            {'codigo': 'RMA', 'nombre': 'Resma', 'simbolo': 'rma'},
        ]

        unidades = {}
        for data in unidades_data:
            unidad, created = UnidadMedida.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'simbolo': data['simbolo'],
                    'activo': True
                }
            )
            unidades[data['codigo']] = unidad
            status = 'Creada' if created else 'Ya existe'
            self.stdout.write(f'  - {status}: {unidad.nombre} ({unidad.simbolo})')

        # ====================== ESTADOS DE ACTIVOS ======================
        self.stdout.write(self.style.MIGRATE_HEADING('\n5. Creando Estados de Activos...'))
        estados_data = [
            {'codigo': 'DISPONIBLE', 'nombre': 'Disponible', 'descripcion': 'Activo disponible para uso', 'color': '#28a745', 'es_inicial': True, 'permite_movimiento': True},
            {'codigo': 'EN_USO', 'nombre': 'En Uso', 'descripcion': 'Activo en uso', 'color': '#17a2b8', 'es_inicial': False, 'permite_movimiento': True},
            {'codigo': 'MANTENIMIENTO', 'nombre': 'En Mantenimiento', 'descripcion': 'Activo en mantenimiento', 'color': '#ffc107', 'es_inicial': False, 'permite_movimiento': False},
            {'codigo': 'REPARACION', 'nombre': 'En Reparacion', 'descripcion': 'Activo en reparacion', 'color': '#fd7e14', 'es_inicial': False, 'permite_movimiento': False},
            {'codigo': 'INACTIVO', 'nombre': 'Inactivo', 'descripcion': 'Activo inactivo o fuera de servicio', 'color': '#6c757d', 'es_inicial': False, 'permite_movimiento': False},
        ]

        estados = {}
        for data in estados_data:
            estado, created = EstadoActivo.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'color': data['color'],
                    'es_inicial': data['es_inicial'],
                    'permite_movimiento': data['permite_movimiento'],
                    'activo': True
                }
            )
            estados[data['codigo']] = estado
            status = 'Creado' if created else 'Ya existe'
            self.stdout.write(f'  - {status}: {estado.nombre}')

        # Obtener el estado por defecto (DISPONIBLE)
        estado_disponible = estados['DISPONIBLE']

        # ====================== CATEGORIAS DE ACTIVOS ======================
        self.stdout.write(self.style.MIGRATE_HEADING('\n6. Creando Categorias de Activos...'))
        categorias_data = [
            {'codigo': 'PAPELERIA', 'nombre': 'Papeleria y Utiles', 'descripcion': 'Articulos de oficina y papeleria'},
            {'codigo': 'LIMPIEZA', 'nombre': 'Productos de Limpieza', 'descripcion': 'Materiales de aseo y limpieza'},
            {'codigo': 'INFORMATICA', 'nombre': 'Informatica', 'descripcion': 'Equipos y accesorios informaticos'},
            {'codigo': 'MOBILIARIO', 'nombre': 'Mobiliario', 'descripcion': 'Muebles y enseres'},
            {'codigo': 'DIDACTICO', 'nombre': 'Material Didactico', 'descripcion': 'Materiales educativos y didacticos'},
        ]

        categorias = {}
        for data in categorias_data:
            cat, created = CategoriaActivo.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'activo': True
                }
            )
            categorias[data['codigo']] = cat
            status = 'Creada' if created else 'Ya existe'
            self.stdout.write(f'  - {status}: {cat.nombre}')

        # ====================== ACTIVOS/ARTICULOS ======================
        self.stdout.write(self.style.MIGRATE_HEADING('\n7. Creando Activos/Articulos...'))
        activos_data = [
            # Papeleria - ARTICULOS (consumibles)
            {'codigo': 'PAP-001', 'nombre': 'Papel Bond Carta', 'categoria': 'PAPELERIA', 'unidad': 'RMA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-002', 'nombre': 'Papel Bond Oficio', 'categoria': 'PAPELERIA', 'unidad': 'RMA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-003', 'nombre': 'Lapiceros Azul', 'categoria': 'PAPELERIA', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-004', 'nombre': 'Lapiceros Negro', 'categoria': 'PAPELERIA', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-005', 'nombre': 'Lapiz Grafito', 'categoria': 'PAPELERIA', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-006', 'nombre': 'Borradores', 'categoria': 'PAPELERIA', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-007', 'nombre': 'Corrector Liquido', 'categoria': 'PAPELERIA', 'unidad': 'UND', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-008', 'nombre': 'Marcadores Permanentes', 'categoria': 'PAPELERIA', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-009', 'nombre': 'Resaltadores', 'categoria': 'PAPELERIA', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-010', 'nombre': 'Folders Manila', 'categoria': 'PAPELERIA', 'unidad': 'PAQ', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-011', 'nombre': 'Cuadernos 100 Hojas', 'categoria': 'PAPELERIA', 'unidad': 'UND', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-012', 'nombre': 'Grapadora', 'categoria': 'PAPELERIA', 'unidad': 'UND', 'tipo': 'BIEN'},
            {'codigo': 'PAP-013', 'nombre': 'Grapas', 'categoria': 'PAPELERIA', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'PAP-014', 'nombre': 'Perforadora', 'categoria': 'PAPELERIA', 'unidad': 'UND', 'tipo': 'BIEN'},
            {'codigo': 'PAP-015', 'nombre': 'Tijeras', 'categoria': 'PAPELERIA', 'unidad': 'UND', 'tipo': 'BIEN'},
            # Limpieza - ARTICULOS (consumibles)
            {'codigo': 'LMP-001', 'nombre': 'Detergente en Polvo', 'categoria': 'LIMPIEZA', 'unidad': 'KG', 'tipo': 'ARTICULO'},
            {'codigo': 'LMP-002', 'nombre': 'Desinfectante', 'categoria': 'LIMPIEZA', 'unidad': 'LT', 'tipo': 'ARTICULO'},
            {'codigo': 'LMP-003', 'nombre': 'Cloro', 'categoria': 'LIMPIEZA', 'unidad': 'LT', 'tipo': 'ARTICULO'},
            {'codigo': 'LMP-004', 'nombre': 'Escobas', 'categoria': 'LIMPIEZA', 'unidad': 'UND', 'tipo': 'BIEN'},
            {'codigo': 'LMP-005', 'nombre': 'Trapeadores', 'categoria': 'LIMPIEZA', 'unidad': 'UND', 'tipo': 'BIEN'},
            {'codigo': 'LMP-006', 'nombre': 'Guantes de Limpieza', 'categoria': 'LIMPIEZA', 'unidad': 'PAQ', 'tipo': 'ARTICULO'},
            {'codigo': 'LMP-007', 'nombre': 'Papel Higienico', 'categoria': 'LIMPIEZA', 'unidad': 'PAQ', 'tipo': 'ARTICULO'},
            {'codigo': 'LMP-008', 'nombre': 'Jabon Liquido', 'categoria': 'LIMPIEZA', 'unidad': 'LT', 'tipo': 'ARTICULO'},
            {'codigo': 'LMP-009', 'nombre': 'Bolsas de Basura', 'categoria': 'LIMPIEZA', 'unidad': 'PAQ', 'tipo': 'ARTICULO'},
            # Informatica - BIENES (inventariables)
            {'codigo': 'INF-001', 'nombre': 'Mouse USB', 'categoria': 'INFORMATICA', 'unidad': 'UND', 'tipo': 'BIEN'},
            {'codigo': 'INF-002', 'nombre': 'Teclado USB', 'categoria': 'INFORMATICA', 'unidad': 'UND', 'tipo': 'BIEN'},
            {'codigo': 'INF-003', 'nombre': 'Cable HDMI', 'categoria': 'INFORMATICA', 'unidad': 'UND', 'tipo': 'ARTICULO'},
            {'codigo': 'INF-004', 'nombre': 'Cable de Red Cat6', 'categoria': 'INFORMATICA', 'unidad': 'MT', 'tipo': 'ARTICULO'},
            {'codigo': 'INF-005', 'nombre': 'USB 32GB', 'categoria': 'INFORMATICA', 'unidad': 'UND', 'tipo': 'BIEN'},
            {'codigo': 'INF-006', 'nombre': 'Disco Duro Externo 1TB', 'categoria': 'INFORMATICA', 'unidad': 'UND', 'tipo': 'BIEN'},
            # Material Didactico - Mixto
            {'codigo': 'DID-001', 'nombre': 'Cartulina de Colores', 'categoria': 'DIDACTICO', 'unidad': 'PAQ', 'tipo': 'ARTICULO'},
            {'codigo': 'DID-002', 'nombre': 'Marcadores para Pizarra', 'categoria': 'DIDACTICO', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
            {'codigo': 'DID-003', 'nombre': 'Pegamento en Barra', 'categoria': 'DIDACTICO', 'unidad': 'UND', 'tipo': 'ARTICULO'},
            {'codigo': 'DID-004', 'nombre': 'Cinta Adhesiva', 'categoria': 'DIDACTICO', 'unidad': 'UND', 'tipo': 'ARTICULO'},
            {'codigo': 'DID-005', 'nombre': 'Plastilina', 'categoria': 'DIDACTICO', 'unidad': 'CJA', 'tipo': 'ARTICULO'},
        ]

        for data in activos_data:
            activo, created = Activo.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'tipo': data['tipo'],
                    'nombre': data['nombre'],
                    'categoria': categorias[data['categoria']],
                    'unidad_medida': unidades[data['unidad']],
                    'estado': estado_disponible,
                    'descripcion': f'{data["nombre"]} para uso general',
                    'activo': True
                }
            )
            status = 'Creado' if created else 'Ya existe'
            self.stdout.write(f'  - {status}: {activo.codigo} - {activo.nombre}')

        # ====================== RESUMEN ======================
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS CREADOS:'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'  Departamentos: {Departamento.objects.count()}')
        self.stdout.write(f'  Areas: {Area.objects.count()}')
        self.stdout.write(f'  Equipos: {Equipo.objects.count()}')
        self.stdout.write(f'  Unidades de Medida: {UnidadMedida.objects.count()}')
        self.stdout.write(f'  Estados de Activos: {EstadoActivo.objects.count()}')
        self.stdout.write(f'  Categorias: {CategoriaActivo.objects.count()}')
        self.stdout.write(f'  Activos/Articulos: {Activo.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('\nSeed completado exitosamente!\n'))
