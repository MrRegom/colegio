"""
Utilidades centralizadas para registro de logs y auditoría.
"""
from typing import Optional
from django.http import HttpRequest
from django.contrib.auth.models import User


def registrar_log_auditoria(
    usuario: User,
    accion_glosa: str,
    descripcion: str,
    request: HttpRequest,
    meta: Optional[dict] = None
) -> None:
    """
    Registra un evento en el log de auditoría del sistema.

    Esta función centraliza el registro de todas las acciones de auditoría
    para evitar duplicación de código y mantener consistencia.

    Args:
        usuario: Usuario que realiza la acción
        accion_glosa: Código de la acción (ej: 'CREAR', 'EDITAR', 'ELIMINAR', 'LOGIN')
        descripcion: Descripción detallada de la acción realizada
        request: Objeto HttpRequest para obtener IP y user-agent
        meta: Diccionario opcional con información adicional en formato JSON

    Returns:
        None

    Example:
        >>> registrar_log_auditoria(
        ...     usuario=request.user,
        ...     accion_glosa='CREAR',
        ...     descripcion='Creó artículo ABC-123',
        ...     request=request,
        ...     meta={'articulo_id': 123}
        ... )
    """
    # Import dentro de la función para evitar dependencias circulares
    from apps.accounts.models import AuthLogs, AuthLogAccion
    from .http import get_client_ip

    try:
        # Obtener o crear la acción
        accion, created = AuthLogAccion.objects.get_or_create(
            glosa=accion_glosa.upper(),
            defaults={'activo': True}
        )

        # Obtener IP del cliente
        ip_usuario = get_client_ip(request)

        # Obtener user agent
        agente = request.META.get('HTTP_USER_AGENT', '')

        # Crear el log
        AuthLogs.objects.create(
            usuario=usuario,
            accion=accion,
            descripcion=descripcion,
            ip_usuario=ip_usuario,
            agente=agente,
            meta=meta
        )

    except Exception as e:
        # Log silencioso - no queremos que falle la operación principal
        # por un error en el logging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(
            f"Error al registrar log de auditoría: {str(e)}",
            exc_info=True,
            extra={
                'usuario': usuario.username if usuario else 'None',
                'accion': accion_glosa,
                'descripcion': descripcion
            }
        )
