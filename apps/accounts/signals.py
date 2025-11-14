import decimal, datetime
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from .models import AuthLogs, AuthLogAccion, HistorialLogin
from .utils import get_client_ip
from .middleware import get_current_user


# --------------------------
#  Señales de Acceso
# --------------------------
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Registra el login exitoso del usuario."""
    ip = get_client_ip(request)
    agente = request.META.get("HTTP_USER_AGENT", "")

    # Obtener session_key si está disponible
    session_key = None
    if hasattr(request, 'session'):
        session_key = request.session.session_key

    # Obtener o crear la acción de login
    accion, created = AuthLogAccion.objects.get_or_create(
        glosa="LOGIN",
        defaults={'activo': True}
    )

    # Crear log de autenticación
    AuthLogs.objects.create(
        accion=accion,
        usuario=user,
        descripcion=f"Usuario {user.username} inició sesión exitosamente.",
        ip_usuario=ip,
        agente=agente,
    )

    # Crear registro en historial de login
    HistorialLogin.objects.create(
        usuario=user,
        session_key=session_key,
        direccion_ip=ip,
        agente=agente,
        fecha_login=timezone.now()
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Registra el logout del usuario."""
    ip = get_client_ip(request)
    agente = request.META.get("HTTP_USER_AGENT", "")

    # Obtener o crear la acción de logout
    accion, created = AuthLogAccion.objects.get_or_create(
        glosa="LOGOUT",
        defaults={'activo': True}
    )

    AuthLogs.objects.create(
        accion=accion,
        usuario=user if user.is_authenticated else None,
        descripcion=f"Usuario {getattr(user, 'username', 'Anónimo')} cerró sesión.",
        ip_usuario=ip,
        agente=agente,
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Registra intentos de login fallidos."""
    ip = get_client_ip(request)
    agente = request.META.get("HTTP_USER_AGENT", "")

    # Obtener o crear la acción de login fallido
    accion, created = AuthLogAccion.objects.get_or_create(
        glosa="LOGIN_FALLIDO",
        defaults={'activo': True}
    )

    AuthLogs.objects.create(
        accion=accion,
        usuario=None,
        descripcion=f"Intento fallido de login con usuario: {credentials.get('username')}",
        ip_usuario=ip,
        agente=agente,
    )

