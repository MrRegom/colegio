"""
Utilidades centralizadas del proyecto.
Estas funciones son reutilizadas en diferentes apps.
"""

from .logging import registrar_log_auditoria
from .http import get_client_ip
from .business import (
    format_rut,
    validar_rut,
    truncar_texto,
    generar_codigo_unico,
)

__all__ = [
    'registrar_log_auditoria',
    'get_client_ip',
    'format_rut',
    'validar_rut',
    'truncar_texto',
    'generar_codigo_unico',
]
