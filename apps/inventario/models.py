"""
Modelos para el módulo de inventario.

IMPORTANTE: Este módulo fue unificado con apps.activos
La mayoría de los modelos han sido migrados o eliminados.

Para más información, ver: PLAN_UNIFICACION_MODULOS.md
"""

from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel


# =================================================================
# MODELOS MIGRADOS A apps.activos
# =================================================================
# Los siguientes modelos fueron migrados al módulo de activos:
# - Taller: Migrado a apps.activos.models.Taller
# - Marca: Migrado a apps.activos.models.Marca
# - Modelo: Migrado a apps.activos.models.Modelo
#
# Para usar estos modelos, importar desde:
#   from apps.activos.models import Taller, Marca, Modelo
# =================================================================


# =================================================================
# MODELOS OBSOLETOS - ELIMINADOS
# =================================================================
# Los siguientes modelos fueron eliminados como parte de la
# unificación de los módulos activos e inventario:
# - TipoEquipo: No necesario
# - Equipo: Reemplazado por apps.activos.models.Activo
# - MantenimientoEquipo: No necesario
# - NombreArticulo: Ya eliminado previamente
# - SectorInventario: Ya eliminado previamente
#
# Si necesita gestionar activos/equipos, use:
#   from apps.activos.models import Activo
# =================================================================
