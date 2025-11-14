from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import AuthEstado, AuthLogAccion


class Command(BaseCommand):
    help = 'Configura datos iniciales: grupos, permisos, acciones de log y superusuario'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuario',
            type=str,
            default='admin',
            help='Usuario para el superusuario (default: admin)'
        )
        parser.add_argument(
            '--correo',
            type=str,
            default='admin@hospital.local',
            help='Correo para el superusuario (default: admin@hospital.local)'
        )
        parser.add_argument(
            '--contrasena',
            type=str,
            default='admin123',
            help='Contraseña para el superusuario (default: admin123)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('Configurando datos iniciales del sistema...')
        )

        # Crear estados de usuario
        self.crear_estados_usuario()
        
        # Crear acciones de log
        self.crear_acciones_log()
        
        # Crear superusuario
        self.crear_superusuario(options)

        self.stdout.write(
            self.style.SUCCESS('Configuración inicial completada exitosamente.')
        )

    def crear_estados_usuario(self):
        """Crear estados básicos de usuario."""
        estados_data = [
            {
                'glosa': 'Activo',
                'activo': True
            },
            {
                'glosa': 'Inactivo',
                'activo': True
            },
            {
                'glosa': 'Bloqueado',
                'activo': True
            }
        ]

        for estado_data in estados_data:
            estado, created = AuthEstado.objects.get_or_create(
                glosa=estado_data['glosa'],
                defaults=estado_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Estado "{estado.glosa}" creado.')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Estado "{estado.glosa}" ya existe.')
                )

    def crear_acciones_log(self):
        """Crear acciones básicas para los logs."""
        acciones_data = [
            {
                'glosa': 'LOGIN',
                'activo': True
            },
            {
                'glosa': 'LOGOUT',
                'activo': True
            },
            {
                'glosa': 'LOGIN_FALLIDO',
                'activo': True
            },
            {
                'glosa': 'CREAR',
                'activo': True
            },
            {
                'glosa': 'ACTUALIZAR',
                'activo': True
            },
            {
                'glosa': 'ELIMINAR',
                'activo': True
            }
        ]

        for accion_data in acciones_data:
            accion, created = AuthLogAccion.objects.get_or_create(
                glosa=accion_data['glosa'],
                defaults=accion_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Acción "{accion.glosa}" creada.')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Acción "{accion.glosa}" ya existe.')
                )

    def crear_superusuario(self, options):
        """Crear superusuario del sistema."""
        # Verificar si ya existe un superusuario
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Ya existe un superusuario en el sistema.')
            )
            return

        try:
            superuser = User.objects.create_superuser(
                username=options['usuario'],
                email=options['correo'],
                password=options['contrasena'],
                first_name='Administrador',
                last_name='del Sistema'
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superusuario "{superuser.username}" creado exitosamente.\n'
                    f'Correo: {superuser.email}\n'
                    f'Para acceder al admin panel: http://localhost:8000/admin/'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al crear superusuario: {str(e)}')
            )
