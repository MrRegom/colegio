from django.db import models
from django.conf import settings
from django.utils import timezone

class AuthEstado(models.Model):
    glosa = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "auth_estado"
        verbose_name = "Estado de usuario"
        verbose_name_plural = "Estados de usuario"
        indexes = [
            models.Index(fields=["activo"]),
        ]


class AuthUserEstado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="estados")
    estado = models.ForeignKey(AuthEstado, on_delete=models.PROTECT, related_name="usuarios")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "auth_user_estado"
        verbose_name = "Estado asignado a usuario"
        verbose_name_plural = "Estados de usuarios"
        # Si quieres que un usuario tenga sólo un estado actual, usa UniqueConstraint
        constraints = [
            models.UniqueConstraint(fields=["usuario"], name="uq_auth_user_estado_user_single", condition=models.Q()),
        ]
        indexes = [
            models.Index(fields=["usuario"]),
            models.Index(fields=["estado"]),
        ]

    def __str__(self):
        return f"{self.usuario} -> {self.estado}"


class AuthLogAccion(models.Model):
    glosa = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "auth_log_accion"
        verbose_name = "Acción de log"
        verbose_name_plural = "Acciones de log"

    def __str__(self):
        return self.glosa


class AuthLogs(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="auth_logs")
    accion = models.ForeignKey(AuthLogAccion, on_delete=models.PROTECT, related_name="logs")
    descripcion = models.TextField(blank=True)
    ip_usuario = models.GenericIPAddressField(null=True, blank=True)
    agente = models.TextField(blank=True)  # user agent
    meta = models.JSONField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_logs"
        verbose_name = "Log de autenticación"
        verbose_name_plural = "Logs de autenticación"
        indexes = [
            models.Index(fields=["usuario"]),
            models.Index(fields=["accion"]),
            models.Index(fields=["-fecha_creacion"]),
        ]

    def __str__(self):
        u = self.usuario if self.usuario else "anon"
        return f"[{self.fecha_creacion}] {u} - {self.accion}"


class HistorialLogin(models.Model):
    """
    Tabla para guardar historial de logins: sesión (clave), IP, user-agent y fecha/hora.
    db_table mantiene el nombre legacy que indicaste: auth_user_login_history
    """
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="login_history",
        db_index=True,
    )
    session_key = models.CharField(
        "clave_sesión",
        max_length=128,
        null=True,
        blank=True,
        help_text="Clave de sesión (session_key). Si existe, puede relacionarse con sesiones_usuarios.id"
    )
    direccion_ip = models.GenericIPAddressField("ip", null=True, blank=True)
    agente = models.TextField("user agent", blank=True, default="")
    fecha_login = models.DateTimeField("fecha_login", default=timezone.now, db_index=True)

    class Meta:
        db_table = "auth_user_login_history"
        verbose_name = "Historial de login"
        verbose_name_plural = "Historiales de login"
        indexes = [
            models.Index(fields=["usuario", "fecha_login"], name="ix_login_usuario_fecha"),
            models.Index(fields=["session_key"], name="ix_login_session_key"),
            models.Index(fields=["direccion_ip", "fecha_login"], name="ix_login_ip_fecha"),
        ]
        ordering = ["-fecha_login"]

    def __str__(self):
        return f"{self.usuario or 'anon'} @ {self.fecha_login.isoformat()} ({self.direccion_ip})"