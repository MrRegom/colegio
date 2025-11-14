from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pages'
    label = 'pages'
    verbose_name = 'Páginas'
    
    def ready(self):
        """Ejecutar configuraciones cuando la app esté lista."""
        pass
