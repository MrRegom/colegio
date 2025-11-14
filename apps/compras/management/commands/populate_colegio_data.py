"""
Comando para poblar la base de datos con datos de ejemplo típicos de un colegio.

Este comando NO modifica la estructura de la base de datos, solo inserta datos nuevos.
Usa get_or_create para evitar duplicados.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo típicos de un colegio (solo inserta, no modifica estructura)'

    def handle(self, *args, **options):
        # Importar modelos
        from apps.bodega.models import Bodega, Categoria, Articulo, UnidadMedida
        from apps.activos.models import (
            CategoriaActivo, EstadoActivo, Marca, Ubicacion, Activo
        )
        from apps.compras.models import Proveedor

        # Obtener usuario admin (debe existir)
        try:
            admin = User.objects.filter(is_superuser=True).first()
            if not admin:
                admin = User.objects.first()
            if not admin:
                self.stdout.write(self.style.ERROR('No hay usuarios en el sistema. Crea un usuario primero.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error obteniendo usuario: {e}'))
            return

        # ==================== PROVEEDORES (10) ====================
        self.stdout.write('Creando proveedores...')
        proveedores_data = [
            {
                'rut': '76.123.456-7',
                'razon_social': 'Librería y Papelería Escolar S.A.',
                'direccion': 'Av. Principal 1234',
                'comuna': 'Santiago',
                'ciudad': 'Santiago',
                'telefono': '+56 2 2345 6789',
                'email': 'contacto@libreriaescolar.cl',
                'sitio_web': 'https://www.libreriaescolar.cl',
            },
            {
                'rut': '76.234.567-8',
                'razon_social': 'Distribuidora de Materiales Didácticos Ltda.',
                'direccion': 'Calle Los Educadores 567',
                'comuna': 'Providencia',
                'ciudad': 'Santiago',
                'telefono': '+56 2 3456 7890',
                'email': 'ventas@materialdidactico.cl',
            },
            {
                'rut': '76.345.678-9',
                'razon_social': 'Equipos Tecnológicos Educativos S.A.',
                'direccion': 'Av. Tecnológica 890',
                'comuna': 'Las Condes',
                'ciudad': 'Santiago',
                'telefono': '+56 2 4567 8901',
                'email': 'info@equipostecno.cl',
                'sitio_web': 'https://www.equipostecno.cl',
            },
            {
                'rut': '76.456.789-0',
                'razon_social': 'Suministros de Aseo y Limpieza Profesional',
                'direccion': 'Pasaje Limpieza 234',
                'comuna': 'Maipú',
                'ciudad': 'Santiago',
                'telefono': '+56 2 5678 9012',
                'email': 'contacto@aseoprofesional.cl',
            },
            {
                'rut': '76.567.890-1',
                'razon_social': 'Cafetería y Alimentación Escolar Ltda.',
                'direccion': 'Av. Alimentación 456',
                'comuna': 'Ñuñoa',
                'ciudad': 'Santiago',
                'telefono': '+56 2 6789 0123',
                'email': 'pedidos@cafeteriaescolar.cl',
            },
            {
                'rut': '76.678.901-2',
                'razon_social': 'Mobiliario Escolar y Oficina S.A.',
                'direccion': 'Calle Muebles 789',
                'comuna': 'San Miguel',
                'ciudad': 'Santiago',
                'telefono': '+56 2 7890 1234',
                'email': 'ventas@mobiliarioescolar.cl',
            },
            {
                'rut': '76.789.012-3',
                'razon_social': 'Uniforme y Textiles Escolares',
                'direccion': 'Av. Textiles 321',
                'comuna': 'La Florida',
                'ciudad': 'Santiago',
                'telefono': '+56 2 8901 2345',
                'email': 'info@uniformescolar.cl',
            },
            {
                'rut': '76.890.123-4',
                'razon_social': 'Materiales de Laboratorio Científico',
                'direccion': 'Pasaje Ciencia 654',
                'comuna': 'Macul',
                'ciudad': 'Santiago',
                'telefono': '+56 2 9012 3456',
                'email': 'laboratorio@materialescientificos.cl',
            },
            {
                'rut': '76.901.234-5',
                'razon_social': 'Equipos Deportivos y Recreación',
                'direccion': 'Av. Deportes 987',
                'comuna': 'Puente Alto',
                'ciudad': 'Santiago',
                'telefono': '+56 2 9123 4567',
                'email': 'deportes@equiposrecreacion.cl',
            },
            {
                'rut': '77.012.345-6',
                'razon_social': 'Servicios de Mantenimiento y Reparación',
                'direccion': 'Calle Mantenimiento 147',
                'comuna': 'Recoleta',
                'ciudad': 'Santiago',
                'telefono': '+56 2 9234 5678',
                'email': 'mantenimiento@serviciosreparacion.cl',
            },
        ]

        proveedores_creados = 0
        for prov_data in proveedores_data:
            obj, created = Proveedor.objects.get_or_create(
                rut=prov_data['rut'],
                defaults={**prov_data, 'activo': True}
            )
            if created:
                proveedores_creados += 1
        self.stdout.write(self.style.SUCCESS(f'[OK] Proveedores: {proveedores_creados} nuevos, {len(proveedores_data) - proveedores_creados} ya existian'))

        # ==================== BODEGAS ====================
        bodega_central, _ = Bodega.objects.get_or_create(
            codigo='BOD01',
            defaults={
                'nombre': 'Bodega Central',
                'descripcion': 'Bodega principal del colegio',
                'responsable': admin,
            }
        )

        # ==================== CATEGORÍAS DE ARTÍCULOS ====================
        categorias_data = [
            {'codigo': 'PAPEL', 'nombre': 'Papelería', 'descripcion': 'Artículos de papelería y escritorio'},
            {'codigo': 'ASEO', 'nombre': 'Aseo y Limpieza', 'descripcion': 'Productos de aseo y limpieza'},
            {'codigo': 'ALIM', 'nombre': 'Alimentación', 'descripcion': 'Productos alimenticios para cocina'},
            {'codigo': 'LAB', 'nombre': 'Laboratorio', 'descripcion': 'Materiales de laboratorio científico'},
        ]

        categorias = {}
        for cat_data in categorias_data:
            cat, _ = Categoria.objects.get_or_create(
                codigo=cat_data['codigo'],
                defaults=cat_data
            )
            categorias[cat_data['codigo']] = cat

        # ==================== UNIDADES DE MEDIDA ====================
        unidades_data = [
            {'codigo': 'UND', 'nombre': 'Unidad', 'simbolo': 'u'},
            {'codigo': 'KG', 'nombre': 'Kilogramo', 'simbolo': 'kg'},
            {'codigo': 'LT', 'nombre': 'Litro', 'simbolo': 'L'},
            {'codigo': 'CAJ', 'nombre': 'Caja', 'simbolo': 'caja'},
            {'codigo': 'PAQ', 'nombre': 'Paquete', 'simbolo': 'paq'},
        ]

        unidades = {}
        for und_data in unidades_data:
            und, _ = UnidadMedida.objects.get_or_create(
                codigo=und_data['codigo'],
                defaults=und_data
            )
            unidades[und_data['codigo']] = und

        # ==================== ARTÍCULOS DE BODEGA (10) ====================
        self.stdout.write('Creando artículos de bodega...')
        articulos_data = [
            {
                'codigo': 'ART-001',
                'nombre': 'Papel A4 500 hojas',
                'descripcion': 'Resma de papel bond A4 blanco',
                'categoria': categorias['PAPEL'],
                'stock_actual': Decimal('150'),
                'stock_minimo': Decimal('20'),
                'stock_maximo': Decimal('500'),
                'punto_reorden': Decimal('30'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-002',
                'nombre': 'Lápices grafito N°2',
                'descripcion': 'Caja de 12 lápices grafito HB',
                'categoria': categorias['PAPEL'],
                'stock_actual': Decimal('45'),
                'stock_minimo': Decimal('10'),
                'stock_maximo': Decimal('200'),
                'punto_reorden': Decimal('15'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-003',
                'nombre': 'Detergente líquido 5L',
                'descripcion': 'Detergente para limpieza general',
                'categoria': categorias['ASEO'],
                'stock_actual': Decimal('8'),
                'stock_minimo': Decimal('5'),
                'stock_maximo': Decimal('50'),
                'punto_reorden': Decimal('8'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-004',
                'nombre': 'Cloro 1L',
                'descripcion': 'Cloro para desinfección de superficies',
                'categoria': categorias['ASEO'],
                'stock_actual': Decimal('12'),
                'stock_minimo': Decimal('5'),
                'stock_maximo': Decimal('30'),
                'punto_reorden': Decimal('8'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-005',
                'nombre': 'Arroz 5kg',
                'descripcion': 'Arroz grano largo para cocina',
                'categoria': categorias['ALIM'],
                'stock_actual': Decimal('25'),
                'stock_minimo': Decimal('10'),
                'stock_maximo': Decimal('100'),
                'punto_reorden': Decimal('15'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-006',
                'nombre': 'Aceite comestible 5L',
                'descripcion': 'Aceite vegetal para cocina',
                'categoria': categorias['ALIM'],
                'stock_actual': Decimal('15'),
                'stock_minimo': Decimal('5'),
                'stock_maximo': Decimal('50'),
                'punto_reorden': Decimal('8'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-007',
                'nombre': 'Microscopio básico',
                'descripcion': 'Microscopio óptico para laboratorio',
                'categoria': categorias['LAB'],
                'stock_actual': Decimal('3'),
                'stock_minimo': Decimal('2'),
                'stock_maximo': Decimal('10'),
                'punto_reorden': Decimal('3'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-008',
                'nombre': 'Gafas de seguridad',
                'descripcion': 'Gafas protectoras para laboratorio',
                'categoria': categorias['LAB'],
                'stock_actual': Decimal('20'),
                'stock_minimo': Decimal('10'),
                'stock_maximo': Decimal('100'),
                'punto_reorden': Decimal('15'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-009',
                'nombre': 'Borradores escolares',
                'descripcion': 'Caja de 50 borradores blancos',
                'categoria': categorias['PAPEL'],
                'stock_actual': Decimal('30'),
                'stock_minimo': Decimal('10'),
                'stock_maximo': Decimal('100'),
                'punto_reorden': Decimal('15'),
                'ubicacion_fisica': bodega_central,
            },
            {
                'codigo': 'ART-010',
                'nombre': 'Tijeras escolares',
                'descripcion': 'Tijeras de punta redonda para estudiantes',
                'categoria': categorias['PAPEL'],
                'stock_actual': Decimal('25'),
                'stock_minimo': Decimal('10'),
                'stock_maximo': Decimal('80'),
                'punto_reorden': Decimal('15'),
                'ubicacion_fisica': bodega_central,
            },
        ]

        articulos_creados = 0
        for art_data in articulos_data:
            # Crear copia para no modificar el original
            art_data_copy = art_data.copy()
            art_obj, created = Articulo.objects.get_or_create(
                codigo=art_data_copy['codigo'],
                defaults=art_data_copy
            )
            if created:
                articulos_creados += 1
                # Asignar unidades de medida por defecto
                art_obj.unidades_medida.add(unidades['UND'])
        self.stdout.write(self.style.SUCCESS(f'[OK] Articulos: {articulos_creados} nuevos, {len(articulos_data) - articulos_creados} ya existian'))

        # ==================== CATEGORÍAS DE ACTIVOS ====================
        cat_activos_data = [
            {'codigo': 'COMP', 'nombre': 'Computadores', 'descripcion': 'Equipos de cómputo'},
            {'codigo': 'MOB', 'nombre': 'Mobiliario', 'descripcion': 'Muebles y mobiliario escolar'},
            {'codigo': 'AUD', 'nombre': 'Audiovisual', 'descripcion': 'Equipos audiovisuales'},
            {'codigo': 'DEP', 'nombre': 'Deportes', 'descripcion': 'Equipos deportivos'},
        ]

        cat_activos = {}
        for cat_data in cat_activos_data:
            cat, _ = CategoriaActivo.objects.get_or_create(
                codigo=cat_data['codigo'],
                defaults=cat_data
            )
            cat_activos[cat_data['codigo']] = cat

        # ==================== ESTADOS DE ACTIVOS ====================
        estado_disponible, _ = EstadoActivo.objects.get_or_create(
            codigo='DISP',
            defaults={
                'nombre': 'Disponible',
                'descripcion': 'Activo disponible para uso',
                'color': '#28a745',
                'es_inicial': True,
                'permite_movimiento': True,
            }
        )

        # ==================== MARCAS ====================
        marcas_data = [
            {'codigo': 'DELL', 'nombre': 'Dell', 'descripcion': 'Marca Dell'},
            {'codigo': 'HP', 'nombre': 'HP', 'descripcion': 'Marca HP'},
            {'codigo': 'LENOVO', 'nombre': 'Lenovo', 'descripcion': 'Marca Lenovo'},
            {'codigo': 'SAMSUNG', 'nombre': 'Samsung', 'descripcion': 'Marca Samsung'},
        ]

        marcas = {}
        for marca_data in marcas_data:
            marca, _ = Marca.objects.get_or_create(
                codigo=marca_data['codigo'],
                defaults=marca_data
            )
            marcas[marca_data['codigo']] = marca

        # ==================== UBICACIONES ====================
        ubicaciones_data = [
            {'codigo': 'LAB-INFO', 'nombre': 'Laboratorio de Informática', 'descripcion': 'Sala de computación'},
            {'codigo': 'BIBLIO', 'nombre': 'Biblioteca', 'descripcion': 'Biblioteca del colegio'},
            {'codigo': 'AULA-101', 'nombre': 'Aula 101', 'descripcion': 'Aula de clases'},
            {'codigo': 'GIMNASIO', 'nombre': 'Gimnasio', 'descripcion': 'Gimnasio deportivo'},
        ]

        ubicaciones = {}
        for ubi_data in ubicaciones_data:
            ubi, _ = Ubicacion.objects.get_or_create(
                codigo=ubi_data['codigo'],
                defaults=ubi_data
            )
            ubicaciones[ubi_data['codigo']] = ubi

        # ==================== ACTIVOS (10) ====================
        self.stdout.write('Creando activos...')
        activos_data = [
            {
                'codigo': 'ACT-001',
                'nombre': 'Laptop Dell Inspiron 15',
                'descripcion': 'Laptop para uso docente',
                'categoria': cat_activos['COMP'],
                'estado': estado_disponible,
                'marca': marcas['DELL'],
                'numero_serie': 'DL123456789',
                'precio_unitario': Decimal('450000'),
            },
            {
                'codigo': 'ACT-002',
                'nombre': 'Proyector Epson',
                'descripcion': 'Proyector multimedia para aulas',
                'categoria': cat_activos['AUD'],
                'estado': estado_disponible,
                'marca': marcas['SAMSUNG'],
                'numero_serie': 'EP987654321',
                'precio_unitario': Decimal('350000'),
            },
            {
                'codigo': 'ACT-003',
                'nombre': 'Pizarra Interactiva',
                'descripcion': 'Pizarra digital interactiva',
                'categoria': cat_activos['AUD'],
                'estado': estado_disponible,
                'precio_unitario': Decimal('1200000'),
            },
            {
                'codigo': 'ACT-004',
                'nombre': 'Escritorio Profesor',
                'descripcion': 'Escritorio para docente',
                'categoria': cat_activos['MOB'],
                'estado': estado_disponible,
                'precio_unitario': Decimal('85000'),
            },
            {
                'codigo': 'ACT-005',
                'nombre': 'Silla Estudiantil',
                'descripcion': 'Silla ergonómica para estudiantes',
                'categoria': cat_activos['MOB'],
                'estado': estado_disponible,
                'precio_unitario': Decimal('25000'),
            },
            {
                'codigo': 'ACT-006',
                'nombre': 'Pelota de Fútbol',
                'descripcion': 'Pelota oficial tamaño 5',
                'categoria': cat_activos['DEP'],
                'estado': estado_disponible,
                'precio_unitario': Decimal('15000'),
            },
            {
                'codigo': 'ACT-007',
                'nombre': 'Tablet Samsung Galaxy',
                'descripcion': 'Tablet para uso educativo',
                'categoria': cat_activos['COMP'],
                'estado': estado_disponible,
                'marca': marcas['SAMSUNG'],
                'numero_serie': 'SG555666777',
                'precio_unitario': Decimal('280000'),
            },
            {
                'codigo': 'ACT-008',
                'nombre': 'Impresora HP LaserJet',
                'descripcion': 'Impresora láser para oficina',
                'categoria': cat_activos['COMP'],
                'estado': estado_disponible,
                'marca': marcas['HP'],
                'numero_serie': 'HP111222333',
                'precio_unitario': Decimal('180000'),
            },
            {
                'codigo': 'ACT-009',
                'nombre': 'Mesa de Ping Pong',
                'descripcion': 'Mesa de tenis de mesa profesional',
                'categoria': cat_activos['DEP'],
                'estado': estado_disponible,
                'precio_unitario': Decimal('250000'),
            },
            {
                'codigo': 'ACT-010',
                'nombre': 'Estantería Biblioteca',
                'descripcion': 'Estantería metálica para libros',
                'categoria': cat_activos['MOB'],
                'estado': estado_disponible,
                'precio_unitario': Decimal('120000'),
            },
        ]

        activos_creados = 0
        for act_data in activos_data:
            act_obj, created = Activo.objects.get_or_create(
                codigo=act_data['codigo'],
                defaults=act_data
            )
            if created:
                activos_creados += 1
        self.stdout.write(self.style.SUCCESS(f'[OK] Activos: {activos_creados} nuevos, {len(activos_data) - activos_creados} ya existian'))

        # ==================== TIPOS Y ESTADOS PARA SOLICITUDES ====================
        from apps.solicitudes.models import TipoSolicitud, EstadoSolicitud, Solicitud, DetalleSolicitud
        from apps.solicitudes.models import Departamento
        
        # Tipos de solicitud
        tipo_normal, _ = TipoSolicitud.objects.get_or_create(
            codigo='NORMAL',
            defaults={
                'nombre': 'Solicitud Normal',
                'descripcion': 'Solicitud estándar',
                'requiere_aprobacion': True,
            }
        )
        
        tipo_urgente, _ = TipoSolicitud.objects.get_or_create(
            codigo='URGENTE',
            defaults={
                'nombre': 'Solicitud Urgente',
                'descripcion': 'Solicitud con prioridad alta',
                'requiere_aprobacion': True,
            }
        )
        
        # Estados de solicitud
        estado_borrador, _ = EstadoSolicitud.objects.get_or_create(
            codigo='BORRADOR',
            defaults={
                'nombre': 'Borrador',
                'descripcion': 'Solicitudes en borrador',
                'color': '#6c757d',
                'es_inicial': True,
                'es_final': False,
                'requiere_accion': False,
            }
        )
        
        estado_en_aprobacion, _ = EstadoSolicitud.objects.get_or_create(
            codigo='EN_APROBACION',
            defaults={
                'nombre': 'En Aprobación',
                'descripcion': 'Solicitudes en proceso de aprobación',
                'color': '#ffc107',
                'es_inicial': False,
                'es_final': False,
                'requiere_accion': True,
            }
        )
        
        estado_aprobada, _ = EstadoSolicitud.objects.get_or_create(
            codigo='APROBADA',
            defaults={
                'nombre': 'Aprobada',
                'descripcion': 'Solicitud aprobada',
                'color': '#28a745',
                'es_inicial': False,
                'es_final': False,
                'requiere_accion': False,
            }
        )
        
        estado_despachada, _ = EstadoSolicitud.objects.get_or_create(
            codigo='DESPACHADA',
            defaults={
                'nombre': 'Despachada',
                'descripcion': 'Solicitud despachada',
                'color': '#007bff',
                'es_inicial': False,
                'es_final': True,
                'requiere_accion': False,
            }
        )
        
        # Departamentos
        dept_docencia, _ = Departamento.objects.get_or_create(
            codigo='DOCENCIA',
            defaults={
                'nombre': 'Docencia',
                'descripcion': 'Departamento de docencia',
                'activo': True,
            }
        )
        
        dept_administracion, _ = Departamento.objects.get_or_create(
            codigo='ADMIN',
            defaults={
                'nombre': 'Administración',
                'descripcion': 'Departamento administrativo',
                'activo': True,
            }
        )
        
        # ==================== SOLICITUDES (10) ====================
        self.stdout.write('Creando solicitudes...')
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        solicitudes_data = [
            {
                'numero': 'SOL-2024-001',
                'tipo': 'ARTICULO',
                'fecha_requerida': timezone.now().date() + timedelta(days=7),
                'tipo_solicitud': tipo_normal,
                'estado': estado_aprobada,
                'titulo_actividad': 'Clases de Ciencias Naturales',
                'objetivo_actividad': 'Realizar experimentos de laboratorio con estudiantes',
                'solicitante': admin,
                'area_solicitante': 'Departamento de Ciencias',
                'departamento': dept_docencia,
                'motivo': 'Necesitamos materiales para las clases prácticas de laboratorio',
                'observaciones': 'Urgente para la próxima semana',
            },
            {
                'numero': 'SOL-2024-002',
                'tipo': 'ARTICULO',
                'fecha_requerida': timezone.now().date() + timedelta(days=3),
                'tipo_solicitud': tipo_urgente,
                'estado': estado_en_aprobacion,
                'titulo_actividad': 'Evento Día del Estudiante',
                'objetivo_actividad': 'Organizar actividades recreativas',
                'solicitante': admin,
                'area_solicitante': 'Coordinación de Actividades',
                'departamento': dept_administracion,
                'motivo': 'Materiales para decoración y actividades del evento',
            },
            {
                'numero': 'SOL-2024-003',
                'tipo': 'ACTIVO',
                'fecha_requerida': timezone.now().date() + timedelta(days=14),
                'tipo_solicitud': tipo_normal,
                'estado': estado_aprobada,
                'titulo_actividad': 'Mejora de Infraestructura Tecnológica',
                'objetivo_actividad': 'Actualizar equipos de computación',
                'solicitante': admin,
                'area_solicitante': 'Informática',
                'departamento': dept_administracion,
                'motivo': 'Necesitamos nuevos equipos para el laboratorio de informática',
            },
            {
                'numero': 'SOL-2024-004',
                'tipo': 'ARTICULO',
                'fecha_requerida': timezone.now().date() + timedelta(days=5),
                'tipo_solicitud': tipo_normal,
                'estado': estado_despachada,
                'titulo_actividad': 'Mantenimiento de Aulas',
                'objetivo_actividad': 'Limpieza y mantenimiento general',
                'solicitante': admin,
                'area_solicitante': 'Mantenimiento',
                'departamento': dept_administracion,
                'motivo': 'Productos de limpieza para mantenimiento mensual',
                'despachador': admin,
                'fecha_despacho': timezone.now() - timedelta(days=2),
            },
            {
                'numero': 'SOL-2024-005',
                'tipo': 'ARTICULO',
                'fecha_requerida': timezone.now().date() + timedelta(days=10),
                'tipo_solicitud': tipo_normal,
                'estado': estado_borrador,
                'titulo_actividad': 'Taller de Arte',
                'objetivo_actividad': 'Actividades artísticas con estudiantes',
                'solicitante': admin,
                'area_solicitante': 'Arte y Cultura',
                'departamento': dept_docencia,
                'motivo': 'Materiales de arte para taller semanal',
            },
            {
                'numero': 'SOL-2024-006',
                'tipo': 'ACTIVO',
                'fecha_requerida': timezone.now().date() + timedelta(days=21),
                'tipo_solicitud': tipo_normal,
                'estado': estado_en_aprobacion,
                'titulo_actividad': 'Renovación de Mobiliario',
                'objetivo_actividad': 'Renovar sillas y mesas de aulas',
                'solicitante': admin,
                'area_solicitante': 'Infraestructura',
                'departamento': dept_administracion,
                'motivo': 'Mobiliario nuevo para mejorar comodidad de estudiantes',
            },
            {
                'numero': 'SOL-2024-007',
                'tipo': 'ARTICULO',
                'fecha_requerida': timezone.now().date() + timedelta(days=1),
                'tipo_solicitud': tipo_urgente,
                'estado': estado_aprobada,
                'titulo_actividad': 'Cocina Escolar',
                'objetivo_actividad': 'Preparación de almuerzos',
                'solicitante': admin,
                'area_solicitante': 'Cocina',
                'departamento': dept_administracion,
                'motivo': 'Insumos alimenticios para la semana',
                'aprobador': admin,
                'fecha_aprobacion': timezone.now() - timedelta(hours=5),
            },
            {
                'numero': 'SOL-2024-008',
                'tipo': 'ARTICULO',
                'fecha_requerida': timezone.now().date() + timedelta(days=6),
                'tipo_solicitud': tipo_normal,
                'estado': estado_aprobada,
                'titulo_actividad': 'Biblioteca Escolar',
                'objetivo_actividad': 'Reposición de materiales de oficina',
                'solicitante': admin,
                'area_solicitante': 'Biblioteca',
                'departamento': dept_docencia,
                'motivo': 'Papelería y materiales de oficina para biblioteca',
            },
            {
                'numero': 'SOL-2024-009',
                'tipo': 'ACTIVO',
                'fecha_requerida': timezone.now().date() + timedelta(days=30),
                'tipo_solicitud': tipo_normal,
                'estado': estado_borrador,
                'titulo_actividad': 'Equipamiento Deportivo',
                'objetivo_actividad': 'Mejorar equipamiento del gimnasio',
                'solicitante': admin,
                'area_solicitante': 'Educación Física',
                'departamento': dept_docencia,
                'motivo': 'Nuevos equipos deportivos para clases',
            },
            {
                'numero': 'SOL-2024-010',
                'tipo': 'ARTICULO',
                'fecha_requerida': timezone.now().date() + timedelta(days=4),
                'tipo_solicitud': tipo_urgente,
                'estado': estado_despachada,
                'titulo_actividad': 'Emergencia Sanitaria',
                'objetivo_actividad': 'Abastecimiento de productos de limpieza',
                'solicitante': admin,
                'area_solicitante': 'Limpieza',
                'departamento': dept_administracion,
                'motivo': 'Reposición urgente de productos de aseo',
                'despachador': admin,
                'fecha_despacho': timezone.now() - timedelta(days=1),
            },
        ]
        
        solicitudes_creadas = 0
        for sol_data in solicitudes_data:
            sol_obj, created = Solicitud.objects.get_or_create(
                numero=sol_data['numero'],
                defaults=sol_data
            )
            if created:
                solicitudes_creadas += 1
                # Crear detalles de solicitud si es de artículos
                if sol_obj.tipo == 'ARTICULO' and sol_obj.estado.codigo in ['APROBADA', 'DESPACHADA']:
                    # Agregar algunos artículos a la solicitud
                    articulos_disponibles = list(Articulo.objects.filter(activo=True, eliminado=False)[:3])
                    for i, articulo in enumerate(articulos_disponibles):
                        DetalleSolicitud.objects.get_or_create(
                            solicitud=sol_obj,
                            articulo=articulo,
                            defaults={
                                'cantidad_solicitada': Decimal(str(5 + i * 2)),
                                'cantidad_aprobada': Decimal(str(5 + i * 2)),
                                'cantidad_despachada': Decimal(str(5 + i * 2)) if sol_obj.estado.codigo == 'DESPACHADA' else Decimal('0'),
                            }
                        )
        self.stdout.write(self.style.SUCCESS(f'[OK] Solicitudes: {solicitudes_creadas} nuevas, {len(solicitudes_data) - solicitudes_creadas} ya existian'))
        
        # ==================== TIPOS DE MOVIMIENTO (BODEGA) ====================
        from apps.bodega.models import TipoMovimiento, Movimiento
        
        tipo_entrada, _ = TipoMovimiento.objects.get_or_create(
            codigo='ENTRADA',
            defaults={
                'nombre': 'Entrada',
                'descripcion': 'Entrada de artículos a bodega',
            }
        )
        
        tipo_salida, _ = TipoMovimiento.objects.get_or_create(
            codigo='SALIDA',
            defaults={
                'nombre': 'Salida',
                'descripcion': 'Salida de artículos de bodega',
            }
        )
        
        tipo_ajuste, _ = TipoMovimiento.objects.get_or_create(
            codigo='AJUSTE',
            defaults={
                'nombre': 'Ajuste',
                'descripcion': 'Ajuste de inventario',
            }
        )
        
        # ==================== MOVIMIENTOS DE ARTÍCULOS (10) ====================
        self.stdout.write('Creando movimientos de articulos...')
        articulos_list = list(Articulo.objects.filter(activo=True, eliminado=False)[:10])
        
        movimientos_creados = 0
        for i, articulo in enumerate(articulos_list):
            # Verificar si ya existe un movimiento similar reciente para este artículo
            fecha_mov = timezone.now() - timedelta(days=10-i if i < 5 else 5-(i-5))
            mov_existente = Movimiento.objects.filter(
                articulo=articulo,
                fecha_creacion__date=fecha_mov.date()
            ).first()
            
            if mov_existente:
                continue  # Ya existe un movimiento para este artículo en esta fecha
            
            if i < 5:
                # Entradas
                stock_antes = articulo.stock_actual
                cantidad = Decimal('10')
                stock_despues = stock_antes + cantidad
                
                mov = Movimiento.objects.create(
                    articulo=articulo,
                    tipo=tipo_entrada,
                    cantidad=cantidad,
                    operacion='ENTRADA',
                    usuario=admin,
                    motivo=f'Recepcion de compra - Lote {i+1}',
                    stock_antes=stock_antes,
                    stock_despues=stock_despues,
                    fecha_creacion=fecha_mov,
                )
            else:
                # Salidas
                stock_antes = articulo.stock_actual
                cantidad = Decimal('5')
                stock_despues = max(Decimal('0'), stock_antes - cantidad)
                
                mov = Movimiento.objects.create(
                    articulo=articulo,
                    tipo=tipo_salida,
                    cantidad=cantidad,
                    operacion='SALIDA',
                    usuario=admin,
                    motivo=f'Entrega para actividad escolar - Solicitud {i-4}',
                    stock_antes=stock_antes,
                    stock_despues=stock_despues,
                    fecha_creacion=fecha_mov,
                )
            
            movimientos_creados += 1
        self.stdout.write(self.style.SUCCESS(f'[OK] Movimientos de articulos: {movimientos_creados} nuevos'))
        
        # ==================== TIPOS DE MOVIMIENTO (ACTIVOS) ====================
        from apps.activos.models import TipoMovimientoActivo, MovimientoActivo, Taller, Proveniencia
        
        tipo_asignacion, _ = TipoMovimientoActivo.objects.get_or_create(
            codigo='ASIGNACION',
            defaults={
                'nombre': 'Asignación',
                'descripcion': 'Asignación de activo a responsable',
            }
        )
        
        tipo_traslado, _ = TipoMovimientoActivo.objects.get_or_create(
            codigo='TRASLADO',
            defaults={
                'nombre': 'Traslado',
                'descripcion': 'Traslado de activo a otra ubicación',
            }
        )
        
        tipo_mantenimiento, _ = TipoMovimientoActivo.objects.get_or_create(
            codigo='MANTENIMIENTO',
            defaults={
                'nombre': 'Mantenimiento',
                'descripcion': 'Envío a mantenimiento',
            }
        )
        
        # Taller
        taller_central, _ = Taller.objects.get_or_create(
            codigo='TAL01',
            defaults={
                'nombre': 'Taller Central',
                'descripcion': 'Taller de mantenimiento general',
                'responsable': admin,
            }
        )
        
        # Proveniencia
        proveniencia_compra, _ = Proveniencia.objects.get_or_create(
            codigo='COMPRA',
            defaults={
                'nombre': 'Compra',
                'descripcion': 'Activo adquirido por compra',
            }
        )
        
        # ==================== MOVIMIENTOS DE ACTIVOS (10) ====================
        self.stdout.write('Creando movimientos de activos...')
        activos_list = list(Activo.objects.filter(activo=True, eliminado=False)[:10])
        ubicaciones_list = list(ubicaciones.values())
        
        movimientos_activos_creados = 0
        for i, activo in enumerate(activos_list):
            # Verificar si ya existe un movimiento reciente para este activo
            fecha_mov = timezone.now() - timedelta(days=15-i)
            mov_existente = MovimientoActivo.objects.filter(
                activo=activo,
                fecha_creacion__date=fecha_mov.date()
            ).first()
            
            if mov_existente:
                continue  # Ya existe un movimiento para este activo en esta fecha
            
            if i < 3:
                # Asignaciones
                tipo_mov = tipo_asignacion
                ubicacion = ubicaciones_list[i % len(ubicaciones_list)] if ubicaciones_list else None
                responsable = admin
                observaciones = f'Asignacion inicial del activo {activo.codigo}'
            elif i < 6:
                # Traslados
                tipo_mov = tipo_traslado
                ubicacion = ubicaciones_list[(i+1) % len(ubicaciones_list)] if ubicaciones_list else None
                responsable = admin
                observaciones = f'Traslado del activo {activo.codigo} a nueva ubicacion'
            else:
                # Mantenimiento
                tipo_mov = tipo_mantenimiento
                ubicacion = None
                responsable = None
                observaciones = f'Envio a mantenimiento preventivo'
            
            mov = MovimientoActivo.objects.create(
                activo=activo,
                tipo_movimiento=tipo_mov,
                usuario_registro=admin,
                ubicacion_destino=ubicacion,
                taller=taller_central if tipo_mov == tipo_mantenimiento else None,
                responsable=responsable,
                proveniencia=proveniencia_compra if i < 3 else None,
                observaciones=observaciones,
                fecha_creacion=fecha_mov,
            )
            
            movimientos_activos_creados += 1
        self.stdout.write(self.style.SUCCESS(f'[OK] Movimientos de activos: {movimientos_activos_creados} nuevos'))
        
        # ==================== RESUMEN ====================
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS CREADOS:'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'[OK] Proveedores: {proveedores_creados} nuevos'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Articulos: {articulos_creados} nuevos'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Activos: {activos_creados} nuevos'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Solicitudes: {solicitudes_creadas} nuevas'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Movimientos de articulos: {movimientos_creados} nuevos'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Movimientos de activos: {movimientos_activos_creados} nuevos'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados exitosamente!'))

