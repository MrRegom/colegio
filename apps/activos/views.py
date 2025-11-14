"""
Vistas del módulo de activos.

Este módulo implementa las vistas para la gestión de activos,
incluyendo CRUD de catálogos y gestión de movimientos.

Todas las vistas usan CBVs (Class-Based Views) y siguen las
mejores prácticas de Django con type hints completos.
"""
from __future__ import annotations

from typing import Any

from django.db.models import QuerySet, Q
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.http import HttpResponse

from core.mixins import (
    BaseAuditedViewMixin, AtomicTransactionMixin, SoftDeleteMixin,
    PaginatedListMixin, FilteredListMixin
)
from .models import (
    Activo, CategoriaActivo, EstadoActivo, Ubicacion,
    Proveniencia, Marca, Taller, TipoMovimientoActivo, MovimientoActivo
)
from .forms import (
    ActivoForm, CategoriaActivoForm, EstadoActivoForm, UbicacionForm,
    ProvenienciaForm, MarcaForm, TallerForm, TipoMovimientoActivoForm,
    MovimientoActivoForm, FiltroActivosForm
)


# ==================== VISTA MENÚ PRINCIPAL ====================

class MenuInventarioView(BaseAuditedViewMixin, TemplateView):
    """
    Vista del menú principal del módulo de inventario (activos).

    Muestra estadísticas y accesos rápidos basados en permisos del usuario.
    Permisos: activos.view_activo
    """
    template_name = 'activos/menu_inventario.html'
    permission_required = 'activos.view_activo'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega estadísticas al contexto."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Estadísticas del módulo
        context['stats'] = {
            'total_activos': Activo.objects.filter(eliminado=False).count(),
            'total_categorias': CategoriaActivo.objects.filter(eliminado=False).count(),
            'total_movimientos': MovimientoActivo.objects.filter(eliminado=False).count(),
            'total_ubicaciones': Ubicacion.objects.filter(eliminado=False).count(),
        }

        # Permisos del usuario
        context['permisos'] = {
            'puede_crear': user.has_perm('activos.add_activo'),
            'puede_movimientos': user.has_perm('activos.add_movimientoactivo'),
            'puede_categorias': user.has_perm('activos.add_categoriaactivo'),
            'puede_gestionar': user.has_perm('activos.change_activo'),
        }

        context['titulo'] = 'Módulo de Inventario'
        return context


# ==================== VISTAS DE ACTIVOS ====================

class ActivoListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """
    Vista para listar activos con filtros y paginación.

    Permisos: activos.view_activo
    Filtros: Categoría, estado, búsqueda por texto
    """
    model = Activo
    template_name = 'activos/lista_activos.html'
    context_object_name = 'activos'
    permission_required = 'activos.view_activo'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Activo]:
        """Retorna activos con optimización N+1."""
        queryset = Activo.objects.filter(eliminado=False).select_related(
            'categoria', 'estado', 'marca'
        )

        # Aplicar filtros del formulario
        form = FiltroActivosForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            # Filtro por categoría
            if data.get('categoria'):
                queryset = queryset.filter(categoria=data['categoria'])

            # Filtro por estado
            if data.get('estado'):
                queryset = queryset.filter(estado=data['estado'])

            # Filtro de búsqueda por texto
            if data.get('buscar'):
                q = data['buscar']
                queryset = queryset.filter(
                    Q(codigo__icontains=q) |
                    Q(nombre__icontains=q) |
                    Q(numero_serie__icontains=q) |
                    Q(codigo_barras__icontains=q)
                )

        return queryset.order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Activos'
        context['form'] = FiltroActivosForm(self.request.GET)
        return context


class ActivoDetailView(BaseAuditedViewMixin, DetailView):
    """
    Vista para ver el detalle de un activo con su historial.

    Permisos: activos.view_activo
    """
    model = Activo
    template_name = 'activos/detalle_activo.html'
    context_object_name = 'activo'
    permission_required = 'activos.view_activo'

    def get_queryset(self) -> QuerySet[Activo]:
        """Optimiza consultas con select_related."""
        return Activo.objects.filter(eliminado=False).select_related(
            'categoria', 'estado', 'marca'
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega movimientos recientes al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Activo {self.object.codigo}'

        # Últimos 10 movimientos del activo
        context['movimientos'] = MovimientoActivo.objects.filter(
            activo=self.object, eliminado=False
        ).select_related(
            'tipo_movimiento', 'ubicacion_destino', 'taller',
            'responsable', 'proveniencia', 'usuario_registro'
        ).order_by('-fecha_creacion')[:10]

        return context


class ActivoCreateView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para crear un nuevo activo.

    Permisos: activos.add_activo
    Auditoría: Registra acción CREAR automáticamente
    Transacción atómica: Garantiza integridad de datos
    """
    model = Activo
    form_class = ActivoForm
    template_name = 'activos/form_activo.html'
    permission_required = 'activos.add_activo'

    # Configuración de auditoría
    audit_action = 'CREAR'
    audit_description_template = 'Creó activo {obj.codigo} - {obj.nombre}'

    # Mensaje de éxito
    success_message = 'Activo {obj.codigo} creado exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle del activo creado."""
        return reverse_lazy('activos:detalle_activo', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Activo'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: ActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class ActivoUpdateView(BaseAuditedViewMixin, AtomicTransactionMixin, UpdateView):
    """
    Vista para editar un activo existente.

    Permisos: activos.change_activo
    Auditoría: Registra acción EDITAR automáticamente
    Transacción atómica: Garantiza integridad de datos
    """
    model = Activo
    form_class = ActivoForm
    template_name = 'activos/form_activo.html'
    permission_required = 'activos.change_activo'

    # Configuración de auditoría
    audit_action = 'EDITAR'
    audit_description_template = 'Editó activo {obj.codigo} - {obj.nombre}'

    # Mensaje de éxito
    success_message = 'Activo {obj.codigo} actualizado exitosamente.'

    def get_queryset(self) -> QuerySet[Activo]:
        """Solo permite editar activos no eliminados."""
        return Activo.objects.filter(eliminado=False)

    def get_success_url(self) -> str:
        """Redirige al detalle del activo editado."""
        return reverse_lazy('activos:detalle_activo', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Activo {self.object.codigo}'
        context['action'] = 'Editar'
        context['activo'] = self.object
        return context

    def form_valid(self, form: ActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class ActivoDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """
    Vista para eliminar (soft delete) un activo.

    Permisos: activos.delete_activo
    Auditoría: Registra acción ELIMINAR automáticamente
    Implementa soft delete (marca como eliminado, no borra físicamente)
    """
    model = Activo
    template_name = 'activos/eliminar_activo.html'
    permission_required = 'activos.delete_activo'
    success_url = reverse_lazy('activos:lista_activos')

    # Configuración de auditoría
    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó activo {obj.codigo} - {obj.nombre}'

    # Mensaje de éxito
    success_message = 'Activo {obj.codigo} eliminado exitosamente.'

    def get_queryset(self) -> QuerySet[Activo]:
        """Solo permite eliminar activos no eliminados."""
        return Activo.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Activo {self.object.codigo}'
        context['activo'] = self.object
        # Verificar si tiene movimientos
        context['tiene_movimientos'] = MovimientoActivo.objects.filter(
            activo=self.object, eliminado=False
        ).exists()
        return context


# ==================== VISTAS DE MOVIMIENTOS ====================

class MovimientoListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """
    Vista para ver el historial de movimientos de inventario con todos los detalles.

    Permisos: activos.view_movimientoactivo
    """
    model = MovimientoActivo
    template_name = 'activos/lista_movimientos.html'
    context_object_name = 'movimientos'
    permission_required = 'activos.view_movimientoactivo'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[MovimientoActivo]:
        """Retorna movimientos con relaciones optimizadas."""
        queryset = MovimientoActivo.objects.filter(eliminado=False).select_related(
            'activo', 'activo__categoria', 'activo__estado', 'activo__marca',
            'tipo_movimiento', 'ubicacion_destino', 'taller', 'responsable',
            'proveniencia', 'usuario_registro'
        )

        # Filtros opcionales
        activo_id = self.request.GET.get('activo')
        if activo_id:
            queryset = queryset.filter(activo_id=activo_id)

        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(activo__categoria_id=categoria_id)

        estado_id = self.request.GET.get('estado')
        if estado_id:
            queryset = queryset.filter(activo__estado_id=estado_id)

        # Filtro de búsqueda
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(activo__codigo__icontains=buscar) |
                Q(activo__nombre__icontains=buscar)
            )

        return queryset.order_by('-fecha_creacion')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Movimientos de Inventario'
        # Agregar catálogos para filtros
        context['categorias'] = CategoriaActivo.objects.filter(activo=True, eliminado=False)
        context['estados'] = EstadoActivo.objects.filter(activo=True, eliminado=False)
        return context


class MovimientoDetailView(BaseAuditedViewMixin, DetailView):
    """
    Vista para ver el detalle de un movimiento.

    Permisos: activos.view_movimientoactivo
    """
    model = MovimientoActivo
    template_name = 'activos/detalle_movimiento.html'
    context_object_name = 'movimiento'
    permission_required = 'activos.view_movimientoactivo'

    def get_queryset(self) -> QuerySet[MovimientoActivo]:
        """Optimiza consultas con select_related."""
        return MovimientoActivo.objects.filter(eliminado=False).select_related(
            'activo', 'tipo_movimiento', 'ubicacion_destino', 'taller',
            'responsable', 'proveniencia', 'usuario_registro'
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Movimiento'
        return context


class MovimientoCreateView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para registrar un nuevo movimiento de activo.

    Permisos: activos.add_movimientoactivo
    Auditoría: Registra acción CREAR automáticamente
    Transacción atómica: Garantiza integridad de datos
    """
    model = MovimientoActivo
    form_class = MovimientoActivoForm
    template_name = 'activos/form_movimiento.html'
    permission_required = 'activos.add_movimientoactivo'
    success_url = reverse_lazy('activos:lista_movimientos')

    # Configuración de auditoría
    audit_action = 'CREAR'
    success_message = 'Movimiento de activo registrado exitosamente.'

    def form_valid(self, form: MovimientoActivoForm) -> HttpResponse:
        """
        Procesa el formulario válido con transacción atómica.

        Asigna el usuario actual como usuario_registro.
        """
        movimiento = form.save(commit=False)
        movimiento.usuario_registro = self.request.user
        movimiento.save()

        self.object = movimiento

        # Generar descripción para auditoría
        descripcion = f'Registró movimiento de activo: {movimiento.activo.codigo}'
        if movimiento.ubicacion_destino:
            descripcion += f' a {movimiento.ubicacion_destino.nombre}'
        if movimiento.responsable:
            descripcion += f' - Responsable: {movimiento.responsable.get_full_name()}'

        self.audit_description_template = descripcion

        # Continuar con el flujo normal (mensaje y redirección)
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Movimiento de Activo'
        context['action'] = 'Registrar'
        return context


# ==================== VISTAS DE CATEGORÍAS ====================

class CategoriaListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """
    Vista para listar categorías de activos.

    Permisos: activos.view_categoriaactivo
    """
    model = CategoriaActivo
    template_name = 'activos/lista_categorias.html'
    context_object_name = 'categorias'
    permission_required = 'activos.view_categoriaactivo'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[CategoriaActivo]:
        """Retorna solo categorías no eliminadas."""
        return CategoriaActivo.objects.filter(eliminado=False).order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Categorías de Activos'
        return context


class CategoriaCreateView(BaseAuditedViewMixin, CreateView):
    """
    Vista para crear una nueva categoría de activo.

    Permisos: activos.add_categoriaactivo
    Auditoría: Registra acción CREAR automáticamente
    """
    model = CategoriaActivo
    form_class = CategoriaActivoForm
    template_name = 'activos/form_categoria.html'
    permission_required = 'activos.add_categoriaactivo'
    success_url = reverse_lazy('activos:lista_categorias')

    # Configuración de auditoría
    audit_action = 'CREAR'
    audit_description_template = 'Creó categoría {obj.codigo} - {obj.nombre}'
    success_message = 'Categoría {obj.nombre} creada exitosamente.'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Categoría'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: CategoriaActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class CategoriaUpdateView(BaseAuditedViewMixin, UpdateView):
    """
    Vista para editar una categoría de activo existente.

    Permisos: activos.change_categoriaactivo
    Auditoría: Registra acción EDITAR automáticamente
    """
    model = CategoriaActivo
    form_class = CategoriaActivoForm
    template_name = 'activos/form_categoria.html'
    permission_required = 'activos.change_categoriaactivo'
    success_url = reverse_lazy('activos:lista_categorias')

    # Configuración de auditoría
    audit_action = 'EDITAR'
    audit_description_template = 'Editó categoría {obj.codigo} - {obj.nombre}'
    success_message = 'Categoría {obj.nombre} actualizada exitosamente.'

    def get_queryset(self) -> QuerySet[CategoriaActivo]:
        """Solo permite editar categorías no eliminadas."""
        return CategoriaActivo.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Categoría {self.object.codigo}'
        context['action'] = 'Editar'
        context['categoria'] = self.object
        return context

    def form_valid(self, form: CategoriaActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class CategoriaDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """
    Vista para eliminar (soft delete) una categoría de activo.

    Permisos: activos.delete_categoriaactivo
    Auditoría: Registra acción ELIMINAR automáticamente
    Implementa soft delete
    """
    model = CategoriaActivo
    template_name = 'activos/eliminar_categoria.html'
    permission_required = 'activos.delete_categoriaactivo'
    success_url = reverse_lazy('activos:lista_categorias')

    # Configuración de auditoría
    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó categoría {obj.codigo} - {obj.nombre}'
    success_message = 'Categoría {obj.codigo} eliminada exitosamente.'

    def get_queryset(self) -> QuerySet[CategoriaActivo]:
        """Solo permite eliminar categorías no eliminadas."""
        return CategoriaActivo.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Categoría {self.object.codigo}'
        context['categoria'] = self.object
        return context


# ==================== VISTAS DE ESTADOS DE ACTIVO ====================

class EstadoActivoListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """Vista para listar estados de activos."""
    model = EstadoActivo
    template_name = 'activos/lista_estados.html'
    context_object_name = 'estados'
    permission_required = 'activos.view_estadoactivo'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[EstadoActivo]:
        """Retorna solo estados no eliminados."""
        return EstadoActivo.objects.filter(eliminado=False).order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Estados de Activos'
        return context


class EstadoActivoCreateView(BaseAuditedViewMixin, CreateView):
    """Vista para crear un nuevo estado de activo."""
    model = EstadoActivo
    form_class = EstadoActivoForm
    template_name = 'activos/form_estado.html'
    permission_required = 'activos.add_estadoactivo'
    success_url = reverse_lazy('activos:lista_estados')

    audit_action = 'CREAR'
    audit_description_template = 'Creó estado {obj.codigo} - {obj.nombre}'
    success_message = 'Estado {obj.nombre} creado exitosamente.'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Estado'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: EstadoActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class EstadoActivoUpdateView(BaseAuditedViewMixin, UpdateView):
    """Vista para editar un estado de activo existente."""
    model = EstadoActivo
    form_class = EstadoActivoForm
    template_name = 'activos/form_estado.html'
    permission_required = 'activos.change_estadoactivo'
    success_url = reverse_lazy('activos:lista_estados')

    audit_action = 'EDITAR'
    audit_description_template = 'Editó estado {obj.codigo} - {obj.nombre}'
    success_message = 'Estado {obj.nombre} actualizado exitosamente.'

    def get_queryset(self) -> QuerySet[EstadoActivo]:
        """Solo permite editar estados no eliminados."""
        return EstadoActivo.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Estado {self.object.codigo}'
        context['action'] = 'Editar'
        context['estado'] = self.object
        return context

    def form_valid(self, form: EstadoActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class EstadoActivoDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """Vista para eliminar (soft delete) un estado de activo."""
    model = EstadoActivo
    template_name = 'activos/eliminar_estado.html'
    permission_required = 'activos.delete_estadoactivo'
    success_url = reverse_lazy('activos:lista_estados')

    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó estado {obj.codigo} - {obj.nombre}'
    success_message = 'Estado {obj.codigo} eliminado exitosamente.'

    def get_queryset(self) -> QuerySet[EstadoActivo]:
        """Solo permite eliminar estados no eliminados."""
        return EstadoActivo.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Estado {self.object.codigo}'
        context['estado'] = self.object
        return context


# ==================== VISTAS DE UBICACIONES ====================

class UbicacionListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """Vista para listar ubicaciones."""
    model = Ubicacion
    template_name = 'activos/lista_ubicaciones.html'
    context_object_name = 'ubicaciones'
    permission_required = 'activos.view_ubicacion'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Ubicacion]:
        """Retorna solo ubicaciones no eliminadas."""
        return Ubicacion.objects.filter(eliminado=False).order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Ubicaciones'
        return context


class UbicacionCreateView(BaseAuditedViewMixin, CreateView):
    """Vista para crear una nueva ubicación."""
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'activos/form_ubicacion.html'
    permission_required = 'activos.add_ubicacion'
    success_url = reverse_lazy('activos:lista_ubicaciones')

    audit_action = 'CREAR'
    audit_description_template = 'Creó ubicación {obj.codigo} - {obj.nombre}'
    success_message = 'Ubicación {obj.nombre} creada exitosamente.'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Ubicación'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: UbicacionForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class UbicacionUpdateView(BaseAuditedViewMixin, UpdateView):
    """Vista para editar una ubicación existente."""
    model = Ubicacion
    form_class = UbicacionForm
    template_name = 'activos/form_ubicacion.html'
    permission_required = 'activos.change_ubicacion'
    success_url = reverse_lazy('activos:lista_ubicaciones')

    audit_action = 'EDITAR'
    audit_description_template = 'Editó ubicación {obj.codigo} - {obj.nombre}'
    success_message = 'Ubicación {obj.nombre} actualizada exitosamente.'

    def get_queryset(self) -> QuerySet[Ubicacion]:
        """Solo permite editar ubicaciones no eliminadas."""
        return Ubicacion.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Ubicación {self.object.codigo}'
        context['action'] = 'Editar'
        context['ubicacion'] = self.object
        return context

    def form_valid(self, form: UbicacionForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class UbicacionDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """Vista para eliminar (soft delete) una ubicación."""
    model = Ubicacion
    template_name = 'activos/eliminar_ubicacion.html'
    permission_required = 'activos.delete_ubicacion'
    success_url = reverse_lazy('activos:lista_ubicaciones')

    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó ubicación {obj.codigo} - {obj.nombre}'
    success_message = 'Ubicación {obj.codigo} eliminada exitosamente.'

    def get_queryset(self) -> QuerySet[Ubicacion]:
        """Solo permite eliminar ubicaciones no eliminadas."""
        return Ubicacion.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Ubicación {self.object.codigo}'
        context['ubicacion'] = self.object
        return context


# ==================== VISTAS DE TIPOS DE MOVIMIENTO ====================

class TipoMovimientoListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """Vista para listar tipos de movimiento."""
    model = TipoMovimientoActivo
    template_name = 'activos/lista_tipos_movimiento.html'
    context_object_name = 'tipos_movimiento'
    permission_required = 'activos.view_tipomovimientoactivo'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[TipoMovimientoActivo]:
        """Retorna solo tipos de movimiento no eliminados."""
        return TipoMovimientoActivo.objects.filter(eliminado=False).order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Tipos de Movimiento'
        return context


class TipoMovimientoCreateView(BaseAuditedViewMixin, CreateView):
    """Vista para crear un nuevo tipo de movimiento."""
    model = TipoMovimientoActivo
    form_class = TipoMovimientoActivoForm
    template_name = 'activos/form_tipo_movimiento.html'
    permission_required = 'activos.add_tipomovimientoactivo'
    success_url = reverse_lazy('activos:lista_tipos_movimiento')

    audit_action = 'CREAR'
    audit_description_template = 'Creó tipo de movimiento {obj.codigo} - {obj.nombre}'
    success_message = 'Tipo de movimiento {obj.nombre} creado exitosamente.'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tipo de Movimiento'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: TipoMovimientoActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class TipoMovimientoUpdateView(BaseAuditedViewMixin, UpdateView):
    """Vista para editar un tipo de movimiento existente."""
    model = TipoMovimientoActivo
    form_class = TipoMovimientoActivoForm
    template_name = 'activos/form_tipo_movimiento.html'
    permission_required = 'activos.change_tipomovimientoactivo'
    success_url = reverse_lazy('activos:lista_tipos_movimiento')

    audit_action = 'EDITAR'
    audit_description_template = 'Editó tipo de movimiento {obj.codigo} - {obj.nombre}'
    success_message = 'Tipo de movimiento {obj.nombre} actualizado exitosamente.'

    def get_queryset(self) -> QuerySet[TipoMovimientoActivo]:
        """Solo permite editar tipos de movimiento no eliminados."""
        return TipoMovimientoActivo.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Tipo de Movimiento {self.object.codigo}'
        context['action'] = 'Editar'
        context['tipo_movimiento'] = self.object
        return context

    def form_valid(self, form: TipoMovimientoActivoForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class TipoMovimientoDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """Vista para eliminar (soft delete) un tipo de movimiento."""
    model = TipoMovimientoActivo
    template_name = 'activos/eliminar_tipo_movimiento.html'
    permission_required = 'activos.delete_tipomovimientoactivo'
    success_url = reverse_lazy('activos:lista_tipos_movimiento')

    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó tipo de movimiento {obj.codigo} - {obj.nombre}'
    success_message = 'Tipo de movimiento {obj.codigo} eliminado exitosamente.'

    def get_queryset(self) -> QuerySet[TipoMovimientoActivo]:
        """Solo permite eliminar tipos de movimiento no eliminados."""
        return TipoMovimientoActivo.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Tipo de Movimiento {self.object.codigo}'
        context['tipo_movimiento'] = self.object
        return context


# ==================== VISTAS DE MARCAS ====================

class MarcaListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """Vista para listar marcas."""
    model = Marca
    template_name = 'activos/lista_marcas.html'
    context_object_name = 'marcas'
    permission_required = 'activos.view_marca'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Marca]:
        """Retorna solo marcas no eliminadas."""
        return Marca.objects.filter(eliminado=False).order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Marcas'
        return context


class MarcaCreateView(BaseAuditedViewMixin, CreateView):
    """Vista para crear una nueva marca."""
    model = Marca
    form_class = MarcaForm
    template_name = 'activos/form_marca.html'
    permission_required = 'activos.add_marca'
    success_url = reverse_lazy('activos:lista_marcas')

    audit_action = 'CREAR'
    audit_description_template = 'Creó marca {obj.codigo} - {obj.nombre}'
    success_message = 'Marca {obj.nombre} creada exitosamente.'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Marca'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: MarcaForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class MarcaUpdateView(BaseAuditedViewMixin, UpdateView):
    """Vista para editar una marca existente."""
    model = Marca
    form_class = MarcaForm
    template_name = 'activos/form_marca.html'
    permission_required = 'activos.change_marca'
    success_url = reverse_lazy('activos:lista_marcas')

    audit_action = 'EDITAR'
    audit_description_template = 'Editó marca {obj.codigo} - {obj.nombre}'
    success_message = 'Marca {obj.nombre} actualizada exitosamente.'

    def get_queryset(self) -> QuerySet[Marca]:
        """Solo permite editar marcas no eliminadas."""
        return Marca.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Marca {self.object.codigo}'
        context['action'] = 'Editar'
        context['marca'] = self.object
        return context

    def form_valid(self, form: MarcaForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class MarcaDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """Vista para eliminar (soft delete) una marca."""
    model = Marca
    template_name = 'activos/eliminar_marca.html'
    permission_required = 'activos.delete_marca'
    success_url = reverse_lazy('activos:lista_marcas')

    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó marca {obj.codigo} - {obj.nombre}'
    success_message = 'Marca {obj.codigo} eliminada exitosamente.'

    def get_queryset(self) -> QuerySet[Marca]:
        """Solo permite eliminar marcas no eliminadas."""
        return Marca.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Marca {self.object.codigo}'
        context['marca'] = self.object
        return context


# ==================== VISTAS DE TALLERES ====================

class TallerListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """Vista para listar talleres."""
    model = Taller
    template_name = 'activos/lista_talleres.html'
    context_object_name = 'talleres'
    permission_required = 'activos.view_taller'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Taller]:
        """Retorna solo talleres no eliminados."""
        return Taller.objects.filter(eliminado=False).select_related('responsable').order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Talleres'
        return context


class TallerCreateView(BaseAuditedViewMixin, CreateView):
    """Vista para crear un nuevo taller."""
    model = Taller
    form_class = TallerForm
    template_name = 'activos/form_taller.html'
    permission_required = 'activos.add_taller'
    success_url = reverse_lazy('activos:lista_talleres')

    audit_action = 'CREAR'
    audit_description_template = 'Creó taller {obj.codigo} - {obj.nombre}'
    success_message = 'Taller {obj.nombre} creado exitosamente.'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Taller'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: TallerForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class TallerUpdateView(BaseAuditedViewMixin, UpdateView):
    """Vista para editar un taller existente."""
    model = Taller
    form_class = TallerForm
    template_name = 'activos/form_taller.html'
    permission_required = 'activos.change_taller'
    success_url = reverse_lazy('activos:lista_talleres')

    audit_action = 'EDITAR'
    audit_description_template = 'Editó taller {obj.codigo} - {obj.nombre}'
    success_message = 'Taller {obj.nombre} actualizado exitosamente.'

    def get_queryset(self) -> QuerySet[Taller]:
        """Solo permite editar talleres no eliminados."""
        return Taller.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Taller {self.object.codigo}'
        context['action'] = 'Editar'
        context['taller'] = self.object
        return context

    def form_valid(self, form: TallerForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class TallerDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """Vista para eliminar (soft delete) un taller."""
    model = Taller
    template_name = 'activos/eliminar_taller.html'
    permission_required = 'activos.delete_taller'
    success_url = reverse_lazy('activos:lista_talleres')

    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó taller {obj.codigo} - {obj.nombre}'
    success_message = 'Taller {obj.codigo} eliminado exitosamente.'

    def get_queryset(self) -> QuerySet[Taller]:
        """Solo permite eliminar talleres no eliminados."""
        return Taller.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Taller {self.object.codigo}'
        context['taller'] = self.object
        return context


# ==================== VISTAS DE PROVENIENCIAS ====================

class ProvenienciaListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """Vista para listar proveniencias."""
    model = Proveniencia
    template_name = 'activos/lista_proveniencias.html'
    context_object_name = 'proveniencias'
    permission_required = 'activos.view_proveniencia'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Proveniencia]:
        """Retorna solo proveniencias no eliminadas."""
        return Proveniencia.objects.filter(eliminado=False).order_by('codigo')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Proveniencias'
        return context


class ProvenienciaCreateView(BaseAuditedViewMixin, CreateView):
    """Vista para crear una nueva proveniencia."""
    model = Proveniencia
    form_class = ProvenienciaForm
    template_name = 'activos/form_proveniencia.html'
    permission_required = 'activos.add_proveniencia'
    success_url = reverse_lazy('activos:lista_proveniencias')

    audit_action = 'CREAR'
    audit_description_template = 'Creó proveniencia {obj.codigo} - {obj.nombre}'
    success_message = 'Proveniencia {obj.nombre} creada exitosamente.'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Proveniencia'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form: ProvenienciaForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class ProvenienciaUpdateView(BaseAuditedViewMixin, UpdateView):
    """Vista para editar una proveniencia existente."""
    model = Proveniencia
    form_class = ProvenienciaForm
    template_name = 'activos/form_proveniencia.html'
    permission_required = 'activos.change_proveniencia'
    success_url = reverse_lazy('activos:lista_proveniencias')

    audit_action = 'EDITAR'
    audit_description_template = 'Editó proveniencia {obj.codigo} - {obj.nombre}'
    success_message = 'Proveniencia {obj.nombre} actualizada exitosamente.'

    def get_queryset(self) -> QuerySet[Proveniencia]:
        """Solo permite editar proveniencias no eliminadas."""
        return Proveniencia.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Proveniencia {self.object.codigo}'
        context['action'] = 'Editar'
        context['proveniencia'] = self.object
        return context

    def form_valid(self, form: ProvenienciaForm) -> HttpResponse:
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class ProvenienciaDeleteView(BaseAuditedViewMixin, SoftDeleteMixin, DeleteView):
    """Vista para eliminar (soft delete) una proveniencia."""
    model = Proveniencia
    template_name = 'activos/eliminar_proveniencia.html'
    permission_required = 'activos.delete_proveniencia'
    success_url = reverse_lazy('activos:lista_proveniencias')

    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó proveniencia {obj.codigo} - {obj.nombre}'
    success_message = 'Proveniencia {obj.codigo} eliminada exitosamente.'

    def get_queryset(self) -> QuerySet[Proveniencia]:
        """Solo permite eliminar proveniencias no eliminadas."""
        return Proveniencia.objects.filter(eliminado=False)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Proveniencia {self.object.codigo}'
        context['proveniencia'] = self.object
        return context


# ==================== NOTA ====================
# Los activos no requieren unidad de medida ya que cada activo es único
# y no maneja cantidades. No existe el modelo UbicacionActual ya que
# la ubicación se rastrea mediante MovimientoActivo.
