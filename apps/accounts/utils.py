"""
Utilidades para el módulo de cuentas.
DEPRECATED: Este módulo se mantiene por compatibilidad hacia atrás.
Usar core.utils en su lugar.
"""
import datetime
import decimal
from django.forms.models import model_to_dict

# Importar desde core.utils (centralizado)
from core.utils import get_client_ip

__all__ = ['get_client_ip']
