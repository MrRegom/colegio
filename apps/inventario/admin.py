"""
Admin para el módulo de inventario.

IMPORTANTE: Los modelos de este módulo fueron migrados o eliminados.
Para gestionar Marca, Modelo y Taller, usar el admin de apps.activos
"""

from django.contrib import admin

# =================================================================
# MODELOS MIGRADOS A apps.activos
# =================================================================
# Los siguientes modelos ahora se gestionan desde apps.activos.admin:
# - Marca
# - Modelo
# - Taller
#
# Los siguientes modelos fueron eliminados (reemplazados por Activo):
# - TipoEquipo
# - Equipo
# - MantenimientoEquipo
# - NombreArticulo
# - SectorInventario
# =================================================================
