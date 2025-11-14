from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    label = 'accounts'  # Label sin puntos para Django
    verbose_name = 'Gestión de Usuarios y Permisos'
    
    def ready(self):
        """Ejecutar configuraciones cuando la app esté lista."""
        # Importar signals para que se registren automáticamente
        from . import signals
