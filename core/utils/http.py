"""
Utilidades HTTP centralizadas.
"""
from typing import Optional
from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
    Obtiene la dirección IP real del cliente desde el request.

    Maneja correctamente proxies y balanceadores de carga revisando
    primero la cabecera X-Forwarded-For.

    Args:
        request: Objeto HttpRequest de Django

    Returns:
        str: Dirección IP del cliente, o None si no se puede determinar

    Example:
        >>> ip = get_client_ip(request)
        >>> print(ip)
        '192.168.1.100'
    """
    if not request:
        return None

    # Revisar si viene de un proxy/load balancer
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For puede contener múltiples IPs separadas por comas
        # La primera es la IP real del cliente
        return x_forwarded_for.split(',')[0].strip()

    # Si no hay proxy, usar REMOTE_ADDR
    return request.META.get('REMOTE_ADDR')
