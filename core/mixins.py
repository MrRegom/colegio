"""
Mixins reutilizables para Class-Based Views.

Estos mixins implementan funcionalidad común siguiendo el principio DRY
y facilitando el mantenimiento del código.

Todos los mixins incluyen type hints completos siguiendo Python 3.13.
"""
from typing import Any, Optional, Dict
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from core.utils import registrar_log_auditoria


class AuditLogMixin:
    """
    Mixin para registrar automáticamente logs de auditoría en operaciones CRUD.

    Attributes:
        audit_action: Acción a registrar ('CREAR', 'EDITAR', 'ELIMINAR', 'LEER')
        audit_description_template: Template para la descripción del log
    """
    audit_action: Optional[str] = None
    audit_description_template: Optional[str] = None

    def get_audit_description(self, obj: Any) -> str:
        """
        Genera la descripción del log de auditoría.

        Args:
            obj: Objeto sobre el cual se realiza la acción

        Returns:
            str: Descripción formateada para el log
        """
        if self.audit_description_template:
            return self.audit_description_template.format(obj=obj)
        return f"{self.audit_action}: {str(obj)}"

    def log_action(self, obj: Any, request: HttpRequest) -> None:
        """
        Registra la acción en el log de auditoría.

        Args:
            obj: Objeto sobre el cual se realiza la acción
            request: HttpRequest actual
        """
        if self.audit_action and hasattr(request, 'user'):
            registrar_log_auditoria(
                usuario=request.user,
                accion_glosa=self.audit_action,
                descripcion=self.get_audit_description(obj),
                request=request
            )


class SuccessMessageMixin:
    """
    Mixin para mostrar mensajes de éxito personalizados.

    Similar a Django's SuccessMessageMixin pero con mejor integración.
    """
    success_message: str = ""

    def get_success_message(self, obj: Any) -> str:
        """
        Genera el mensaje de éxito basado en el objeto.

        Args:
            obj: Objeto sobre el cual se realizó la operación

        Returns:
            str: Mensaje de éxito formateado
        """
        if self.success_message:
            return self.success_message.format(obj=obj)
        return f"Operación exitosa: {str(obj)}"

    def form_valid(self, form) -> HttpResponse:
        """
        Sobrescribe form_valid para agregar mensaje de éxito.

        Args:
            form: Formulario validado

        Returns:
            HttpResponse: Respuesta HTTP
        """
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(self.object))
        return response


class AtomicTransactionMixin:
    """
    Mixin para envolver operaciones en transacciones atómicas.

    Garantiza que todas las operaciones de la vista se ejecuten
    de manera atómica (todo o nada).
    """
    @transaction.atomic
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Envuelve el dispatch en una transacción atómica.

        Args:
            request: HttpRequest de Django
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados

        Returns:
            HttpResponse: Respuesta HTTP
        """
        return super().dispatch(request, *args, **kwargs)


class SoftDeleteMixin:
    """
    Mixin para implementar soft delete en lugar de eliminación física.

    En lugar de eliminar el registro de la base de datos, marca
    el campo 'eliminado' como True.
    """
    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Sobrescribe delete para hacer soft delete.

        En lugar de eliminar el objeto, marca eliminado=True.

        Args:
            request: HttpRequest de Django
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados

        Returns:
            HttpResponse: Redirección a success_url
        """
        self.object = self.get_object()
        self.object.eliminado = True
        self.object.activo = False
        self.object.save()

        success_url: str = str(self.get_success_url())

        # Mensaje y log de auditoría
        if hasattr(self, 'get_success_message'):
            messages.success(request, self.get_success_message(self.object))

        if hasattr(self, 'log_action'):
            self.log_action(self.object, request)

        return HttpResponse(status=302, headers={'Location': success_url})


class BaseAuditedViewMixin(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    AuditLogMixin,
    SuccessMessageMixin
):
    """
    Mixin base que combina autenticación, permisos, auditoría y mensajes.

    Este es el mixin principal para usar en vistas que requieren:
    - Usuario autenticado
    - Verificación de permisos
    - Log de auditoría automático
    - Mensajes de éxito
    """
    pass


class PaginatedListMixin:
    """
    Mixin para agregar paginación automática a ListView.

    Attributes:
        paginate_by: Número de elementos por página (default: 25)
        paginate_orphans: Elementos huérfanos que se agregan a la última página
    """
    paginate_by: int = 25
    paginate_orphans: int = 5

    def get_paginate_by(self, queryset: QuerySet) -> int:
        """
        Permite override dinámico de paginate_by.

        Puede ser sobreescrito para permitir paginación dinámica
        basada en parámetros GET, por ejemplo.

        Args:
            queryset: QuerySet a paginar

        Returns:
            int: Número de elementos por página
        """
        # Permitir override desde query params
        try:
            per_page_str: Optional[str] = self.request.GET.get('per_page')
            if per_page_str:
                per_page: int = int(per_page_str)
                if 1 <= per_page <= 100:  # Límite de seguridad
                    return per_page
        except (ValueError, TypeError):
            pass

        return self.paginate_by


class FilteredListMixin:
    """
    Mixin para agregar filtros a ListView.

    Attributes:
        filter_form_class: Clase del formulario de filtros
        filter_fields: Campos por los cuales filtrar
    """
    filter_form_class: Optional[type] = None
    filter_fields: list[str] = []

    def get_queryset(self) -> QuerySet:
        """
        Aplica filtros al queryset base.

        Returns:
            QuerySet: QuerySet filtrado
        """
        queryset: QuerySet = super().get_queryset()

        if self.filter_form_class:
            form = self.filter_form_class(self.request.GET)
            if form.is_valid():
                queryset = self.apply_filters(queryset, form.cleaned_data)

        return queryset

    def apply_filters(self, queryset: QuerySet, filters: Dict[str, Any]) -> QuerySet:
        """
        Aplica los filtros al queryset.

        Args:
            queryset: QuerySet base
            filters: Dict con los filtros del formulario

        Returns:
            QuerySet: QuerySet filtrado
        """
        for field, value in filters.items():
            if value:
                queryset = queryset.filter(**{field: value})

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Agrega el formulario de filtros al contexto.

        Args:
            **kwargs: Argumentos del contexto

        Returns:
            Dict[str, Any]: Contexto actualizado
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)

        if self.filter_form_class:
            context['filter_form'] = self.filter_form_class(self.request.GET)

        return context
