"""
Comando de management para cargar datos de prueba en los gestores.
Ejecutar: python manage.py seed_gestores
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.inventario.models import Taller, TipoEquipo, Equipo
from apps.bodega.models import Bodega
from apps.compras.models import EstadoOrdenCompra, EstadoRecepcion
from apps.activos.models import Proveniencia
from apps.solicitudes.models import Departamento


class Command(BaseCommand):
    help = 'Carga datos de prueba para los gestores de inventario'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando carga de datos de prueba...'))
        
        # Obtener o crear un usuario para las relaciones
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@colegio.local', 'is_staff': True, 'is_superuser': True}
        )
        if not user.is_superuser:
            user.set_password('admin123')
            user.save()

        # ==================== TALLERES ====================
        self.stdout.write('Creando talleres...')
        talleres_data = [
            {'codigo': 'TAL-001', 'nombre': 'Taller de Tecnología', 'ubicacion': 'Edificio A, Piso 2'},
            {'codigo': 'TAL-002', 'nombre': 'Taller de Artes', 'ubicacion': 'Edificio B, Piso 1'},
            {'codigo': 'TAL-003', 'nombre': 'Taller de Ciencias', 'ubicacion': 'Edificio C, Piso 2'},
            {'codigo': 'TAL-004', 'nombre': 'Taller de Música', 'ubicacion': 'Edificio A, Piso 1'},
        ]
        
        for data in talleres_data:
            Taller.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'ubicacion': data['ubicacion'],
                    'responsable': user,
                    'capacidad_maxima': 30,
                    'activo': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(talleres_data)} talleres creados'))

        # ==================== TIPOS DE EQUIPO ====================
        self.stdout.write('Creando tipos de equipo...')
        tipos_equipo_data = [
            {'codigo': 'TEQ-001', 'nombre': 'Computadores', 'requiere_mantenimiento': True, 'periodo_mantenimiento_dias': 180},
            {'codigo': 'TEQ-002', 'nombre': 'Proyectores', 'requiere_mantenimiento': True, 'periodo_mantenimiento_dias': 90},
            {'codigo': 'TEQ-003', 'nombre': 'Impresoras', 'requiere_mantenimiento': True, 'periodo_mantenimiento_dias': 120},
            {'codigo': 'TEQ-004', 'nombre': 'Equipos de Audio', 'requiere_mantenimiento': False},
        ]
        
        for data in tipos_equipo_data:
            TipoEquipo.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'requiere_mantenimiento': data.get('requiere_mantenimiento', False),
                    'periodo_mantenimiento_dias': data.get('periodo_mantenimiento_dias'),
                    'activo': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(tipos_equipo_data)} tipos de equipo creados'))

        # ==================== BODEGAS ====================
        self.stdout.write('Creando bodegas...')
        bodegas_data = [
            {'codigo': 'BOD-001', 'nombre': 'Bodega Principal', 'descripcion': 'Bodega principal del colegio'},
            {'codigo': 'BOD-002', 'nombre': 'Bodega de Material Didáctico', 'descripcion': 'Materiales educativos'},
            {'codigo': 'BOD-003', 'nombre': 'Bodega de Informática', 'descripcion': 'Equipos y materiales de informática'},
        ]
        
        for data in bodegas_data:
            Bodega.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'responsable': user,
                    'activo': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(bodegas_data)} bodegas creadas'))

        # ==================== DEPARTAMENTOS ====================
        self.stdout.write('Creando departamentos...')
        departamentos_data = [
            {'codigo': 'DEP-001', 'nombre': 'Dirección', 'descripcion': 'Dirección General'},
            {'codigo': 'DEP-002', 'nombre': 'Académico', 'descripcion': 'Departamento Académico'},
            {'codigo': 'DEP-003', 'nombre': 'Administración', 'descripcion': 'Administración y Finanzas'},
            {'codigo': 'DEP-004', 'nombre': 'Tecnología', 'descripcion': 'Departamento de Tecnología'},
        ]
        
        for data in departamentos_data:
            Departamento.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'responsable': user,
                    'activo': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(departamentos_data)} departamentos creados'))

        # ==================== ESTADOS DE ORDEN DE COMPRA ====================
        self.stdout.write('Creando estados de orden de compra...')
        estados_oc_data = [
            {'codigo': 'EOC-001', 'nombre': 'Pendiente', 'color': '#ffc107', 'es_inicial': True, 'permite_edicion': True},
            {'codigo': 'EOC-002', 'nombre': 'Aprobada', 'color': '#17a2b8', 'permite_edicion': True},
            {'codigo': 'EOC-003', 'nombre': 'En Compra', 'color': '#007bff', 'permite_edicion': False},
            {'codigo': 'EOC-004', 'nombre': 'Recibida', 'color': '#28a745', 'es_final': True, 'permite_edicion': False},
            {'codigo': 'EOC-005', 'nombre': 'Cancelada', 'color': '#dc3545', 'es_final': True, 'permite_edicion': False},
        ]
        
        for data in estados_oc_data:
            EstadoOrdenCompra.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'color': data['color'],
                    'es_inicial': data.get('es_inicial', False),
                    'es_final': data.get('es_final', False),
                    'permite_edicion': data.get('permite_edicion', True),
                    'activo': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(estados_oc_data)} estados de orden de compra creados'))

        # ==================== ESTADOS DE RECEPCIÓN ====================
        self.stdout.write('Creando estados de recepción...')
        estados_rec_data = [
            {'codigo': 'ERC-001', 'nombre': 'Pendiente', 'color': '#ffc107', 'es_inicial': True},
            {'codigo': 'ERC-002', 'nombre': 'En Proceso', 'color': '#17a2b8'},
            {'codigo': 'ERC-003', 'nombre': 'Completada', 'color': '#28a745', 'es_final': True},
        ]
        
        for data in estados_rec_data:
            EstadoRecepcion.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'color': data['color'],
                    'es_inicial': data.get('es_inicial', False),
                    'es_final': data.get('es_final', False),
                    'activo': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(estados_rec_data)} estados de recepción creados'))

        # ==================== PROVENIENCIAS ====================
        self.stdout.write('Creando proveniencias...')
        proveniencias_data = [
            {'codigo': 'PRO-001', 'nombre': 'Compra', 'descripcion': 'Activo adquirido por compra'},
            {'codigo': 'PRO-002', 'nombre': 'Donación', 'descripcion': 'Activo recibido por donación'},
            {'codigo': 'PRO-003', 'nombre': 'Transferencia', 'descripcion': 'Transferido desde otra institución'},
            {'codigo': 'PRO-004', 'nombre': 'Fabricación Propia', 'descripcion': 'Elaborado en el colegio'},
        ]
        
        for data in proveniencias_data:
            Proveniencia.objects.get_or_create(
                codigo=data['codigo'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'activo': True
                }
            )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(proveniencias_data)} proveniencias creadas'))

        self.stdout.write(self.style.SUCCESS('\n✓ ¡Datos de prueba cargados exitosamente!'))
        self.stdout.write(self.style.WARNING('\nNota: Algunos templates aún faltan. Revisa RESUMEN_GESTORES_COMPLETO.md'))

