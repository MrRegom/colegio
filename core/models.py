from django.db import models
from django.conf import settings

# Create your models here.


class BaseModel(models.Model):
    """
    Modelo base para auditoría - todos los modelos heredan de esta clase
    """
    activo = models.BooleanField(default=True, verbose_name="Activo", help_text="Estado activo/inactivo del registro")
    eliminado = models.BooleanField(default=False, verbose_name="Eliminado", help_text="Estado eliminado/no eliminado del registro")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación", help_text="Fecha y hora de creación del registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización", help_text="Fecha y hora de última actualización")

    class Meta:
        abstract = True

