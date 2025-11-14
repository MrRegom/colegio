"""
Class-Based Views para el módulo de solicitudes.

Este archivo implementa todas las vistas usando CBVs siguiendo SOLID y DRY:
- Reutilización de mixins de core.mixins
- Separación de responsabilidades (Repository Pattern + Service Layer)
- Código limpio y mantenible
- Type hints completos
- Auditoría automática
- Workflow de aprobación y despacho
"""
from typing import Any
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from core.mixins import (
    BaseAuditedViewMixin, AtomicTransactionMixin, SoftDeleteMixin,
    PaginatedListMixin, FilteredListMixin
)
from core.utils import registrar_log_auditoria
from .models import Solicitud, TipoSolicitud, EstadoSolicitud, DetalleSolicitud, HistorialSolicitud
from .forms import (
    SolicitudForm, DetalleSolicitudArticuloFormSet, DetalleSolicitudActivoFormSet,
    AprobarSolicitudForm, DespacharSolicitudForm, RechazarSolicitudForm,
    FiltroSolicitudesForm
)
from .repositories import (
    TipoSolicitudRepository, EstadoSolicitudRepository, SolicitudRepository,
    DetalleSolicitudRepository, HistorialSolicitudRepository
)
from .services import SolicitudService, DetalleSolicitudService
from decimal import Decimal


# ==================== VISTA MENÚ PRINCIPAL ====================

class MenuSolicitudesView(BaseAuditedViewMixin, TemplateView):
    """
    Vista del menú principal del módulo de solicitudes.

    Muestra estadísticas y accesos rápidos basados en permisos del usuario.
    Permisos: solicitudes.view_solicitud
    Utiliza: Repositories para acceso a datos optimizado
    """
    template_name = 'solicitudes/menu_solicitudes.html'
    permission_required = 'solicitudes.view_solicitud'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega estadísticas y permisos al contexto usando repositories."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Inicializar repositories
        solicitud_repo = SolicitudRepository()
        estado_repo = EstadoSolicitudRepository()

        # Estadísticas del módulo usando repositories
        estado_pendiente = estado_repo.get_by_codigo('PENDIENTE')
        pendientes_count = 0
        if estado_pendiente:
            pendientes_count = solicitud_repo.filter_by_estado(estado_pendiente).count()

        context['stats'] = {
            'total_solicitudes': solicitud_repo.get_all().count(),
            'mis_solicitudes': solicitud_repo.filter_by_solicitante(user).count(),
            'solicitudes_activos': solicitud_repo.filter_by_tipo_choice('ACTIVO').count(),
            'solicitudes_articulos': solicitud_repo.filter_by_tipo_choice('ARTICULO').count(),
            'pendientes': pendientes_count,
        }

        # Permisos del usuario
        context['permisos'] = {
            'puede_crear': user.has_perm('solicitudes.add_solicitud'),
            'puede_aprobar': user.has_perm('solicitudes.aprobar_solicitud'),
            'puede_gestionar': user.has_perm('solicitudes.change_solicitud'),
        }

        context['titulo'] = 'Módulo de Solicitudes'
        return context


# ==================== VISTAS DE SOLICITUDES GENERALES ====================

class SolicitudListView(BaseAuditedViewMixin, PaginatedListMixin, FilteredListMixin, ListView):
    """
    Vista para listar todas las solicitudes con filtros.

    Permisos: solicitudes.view_solicitud
    Filtros: Estado, tipo, fechas, búsqueda
    """
    model = Solicitud
    template_name = 'solicitudes/lista_solicitudes.html'
    context_object_name = 'solicitudes'
    permission_required = 'solicitudes.view_solicitud'
    paginate_by = 25
    filter_form_class = FiltroSolicitudesForm

    def get_queryset(self) -> QuerySet:
        """Retorna solicitudes con relaciones optimizadas y filtros."""
        queryset = super().get_queryset().select_related(
            'tipo_solicitud', 'estado', 'solicitante', 'bodega_origen'
        )

        # Aplicar filtros del formulario
        form = self.filter_form_class(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('estado'):
                queryset = queryset.filter(estado=data['estado'])

            if data.get('tipo'):
                queryset = queryset.filter(tipo_solicitud=data['tipo'])

            if data.get('fecha_desde'):
                queryset = queryset.filter(fecha_solicitud__gte=data['fecha_desde'])

            if data.get('fecha_hasta'):
                queryset = queryset.filter(fecha_solicitud__lte=data['fecha_hasta'])

            if data.get('buscar'):
                q = data['buscar']
                queryset = queryset.filter(
                    Q(numero__icontains=q) |
                    Q(solicitante__username__icontains=q) |
                    Q(area_solicitante__icontains=q)
                )

        return queryset.order_by('-fecha_solicitud')

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Solicitudes'
        context['form'] = self.filter_form_class(self.request.GET)
        return context


class SolicitudDetailView(BaseAuditedViewMixin, DetailView):
    """
    Vista para ver el detalle de una solicitud.

    Permisos: solicitudes.view_solicitud
    """
    model = Solicitud
    template_name = 'solicitudes/detalle_solicitud.html'
    context_object_name = 'solicitud'
    permission_required = 'solicitudes.view_solicitud'

    def get_queryset(self) -> QuerySet:
        """Optimiza consultas con select_related."""
        return super().get_queryset().select_related(
            'tipo_solicitud', 'estado', 'solicitante', 'aprobador',
            'despachador', 'bodega_origen'
        )

    def get_context_data(self, **kwargs) -> dict:
        """Agrega detalles y historial al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Solicitud {self.object.numero}'

        # Detalles de la solicitud
        # No usamos select_related porque DetalleSolicitud puede tener articulo O activo
        # Django hará queries lazy loading según corresponda
        context['detalles'] = self.object.detalles.filter(eliminado=False).select_related(
            'articulo',  # Para artículos de bodega
            'articulo__categoria',
            'activo',  # Para activos/bienes de inventario
            'activo__categoria'
        ).order_by('id')

        # Historial de cambios
        context['historial'] = self.object.historial.select_related(
            'estado_anterior', 'estado_nuevo', 'usuario'
        )

        return context


class MisSolicitudesListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """
    Vista para ver las solicitudes del usuario actual.

    Permisos: solicitudes.view_solicitud
    """
    model = Solicitud
    template_name = 'solicitudes/mis_solicitudes.html'
    context_object_name = 'solicitudes'
    permission_required = 'solicitudes.view_solicitud'
    paginate_by = 25

    def get_queryset(self) -> QuerySet:
        """Retorna solo las solicitudes del usuario actual."""
        return super().get_queryset().filter(
            solicitante=self.request.user
        ).select_related(
            'tipo_solicitud', 'estado', 'bodega_origen'
        ).order_by('-fecha_solicitud')

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Mis Solicitudes'
        return context


class SolicitudCreateView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para crear una nueva solicitud.

    Permisos: solicitudes.add_solicitud
    Auditoría: Registra acción CREAR automáticamente
    Transacción atómica: Garantiza que solicitud y detalles se creen correctamente
    """
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudes/form_solicitud.html'
    permission_required = 'solicitudes.add_solicitud'

    # Configuración de auditoría
    audit_action = 'CREAR'
    audit_description_template = 'Creó solicitud {obj.numero}'

    # Mensaje de éxito
    success_message = 'Solicitud {obj.numero} creada exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la solicitud creada."""
        return reverse_lazy('solicitudes:detalle_solicitud', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega formset y datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Solicitud'
        context['action'] = 'Crear'

        # Las vistas hijas deben sobrescribir esto con el formset correcto
        if self.request.POST:
            context['formset'] = DetalleSolicitudActivoFormSet(self.request.POST)
        else:
            context['formset'] = DetalleSolicitudActivoFormSet()

        return context

    def form_valid(self, form):
        """Procesa el formulario válido usando SolicitudService."""
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            solicitud_service = SolicitudService()

            try:
                # Crear solicitud usando service
                self.object = solicitud_service.crear_solicitud(
                    tipo_solicitud=form.cleaned_data['tipo_solicitud'],
                    solicitante=self.request.user,
                    fecha_requerida=form.cleaned_data['fecha_requerida'],
                    motivo=form.cleaned_data['motivo'],
                    area_solicitante=form.cleaned_data['area_solicitante'],
                    titulo_actividad=form.cleaned_data.get('titulo_actividad', ''),
                    objetivo_actividad=form.cleaned_data.get('objetivo_actividad', ''),
                    tipo_choice=form.cleaned_data.get('tipo', 'ARTICULO'),
                    bodega_origen=form.cleaned_data.get('bodega_origen'),
                    departamento=form.cleaned_data.get('departamento'),
                    area=form.cleaned_data.get('area'),
                    equipo=form.cleaned_data.get('equipo'),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )

                # Guardar los detalles
                formset.instance = self.object
                formset.save()

                # Mensaje de éxito y log de auditoría
                messages.success(self.request, self.get_success_message(self.object))
                self.log_action(self.object, self.request)

                return redirect(self.get_success_url())

            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class SolicitudUpdateView(BaseAuditedViewMixin, AtomicTransactionMixin, UpdateView):
    """
    Vista para editar una solicitud existente.

    Permisos: solicitudes.change_solicitud
    Auditoría: Registra acción EDITAR automáticamente
    Transacción atómica: Garantiza consistencia de datos
    """
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitudes/form_solicitud.html'
    permission_required = 'solicitudes.change_solicitud'

    # Configuración de auditoría
    audit_action = 'EDITAR'
    audit_description_template = 'Editó solicitud {obj.numero}'

    # Mensaje de éxito
    success_message = 'Solicitud {obj.numero} actualizada exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la solicitud editada."""
        return reverse_lazy('solicitudes:detalle_solicitud', kwargs={'pk': self.object.pk})

    def get_queryset(self) -> QuerySet:
        """Filtra solicitudes según permisos del usuario."""
        queryset = super().get_queryset()

        # Si no tiene permiso para editar cualquier solicitud, solo las propias
        if not self.request.user.has_perm('solicitudes.change_any_solicitud'):
            queryset = queryset.filter(solicitante=self.request.user)

        return queryset

    def get(self, request, *args, **kwargs):
        """Verifica que la solicitud pueda ser editada."""
        self.object = self.get_object()

        # Verificar permisos de edición
        if self.object.solicitante != request.user and not request.user.has_perm('solicitudes.change_any_solicitud'):
            messages.error(request, 'No tiene permisos para editar esta solicitud.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        # No permitir edición si ya fue aprobada o despachada
        if self.object.estado.es_final:
            messages.warning(request, 'No se puede editar una solicitud en estado final.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        """Agrega formset y datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Solicitud {self.object.numero}'
        context['action'] = 'Editar'
        context['solicitud'] = self.object

        # Seleccionar el formset correcto según el tipo de solicitud
        if self.object.tipo == 'ARTICULO':
            context['tipo'] = 'ARTICULO'
            if self.request.POST:
                context['formset'] = DetalleSolicitudArticuloFormSet(self.request.POST, instance=self.object)
            else:
                context['formset'] = DetalleSolicitudArticuloFormSet(instance=self.object)
        else:  # ACTIVO
            context['tipo'] = 'ACTIVO'
            if self.request.POST:
                context['formset'] = DetalleSolicitudActivoFormSet(self.request.POST, instance=self.object)
            else:
                context['formset'] = DetalleSolicitudActivoFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        """Procesa el formulario válido con formset."""
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            form.save()
            formset.save()

            # Continuar con el flujo normal (mensaje y redirección)
            response = super().form_valid(form)
            self.log_action(self.object, self.request)
            return response
        else:
            return self.form_invalid(form)


class SolicitudDeleteView(BaseAuditedViewMixin, AtomicTransactionMixin, DeleteView):
    """
    Vista para eliminar una solicitud.

    Permisos: solicitudes.delete_solicitud
    Auditoría: Registra acción ELIMINAR automáticamente
    Transacción atómica: Garantiza consistencia
    """
    model = Solicitud
    template_name = 'solicitudes/eliminar_solicitud.html'
    permission_required = 'solicitudes.delete_solicitud'
    success_url = reverse_lazy('solicitudes:lista_solicitudes')

    # Configuración de auditoría
    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó solicitud {obj.numero}'

    # Mensaje de éxito
    success_message = 'Solicitud {obj.numero} eliminada exitosamente.'

    def get_queryset(self) -> QuerySet:
        """Filtra solicitudes según permisos del usuario."""
        queryset = super().get_queryset()

        # Si no tiene permiso para eliminar cualquier solicitud, solo las propias
        if not self.request.user.has_perm('solicitudes.delete_any_solicitud'):
            queryset = queryset.filter(solicitante=self.request.user)

        return queryset

    def get(self, request, *args, **kwargs):
        """Verifica que la solicitud pueda ser eliminada."""
        self.object = self.get_object()

        # Verificar permisos de eliminación
        if self.object.solicitante != request.user and not request.user.has_perm('solicitudes.delete_any_solicitud'):
            messages.error(request, 'No tiene permisos para eliminar esta solicitud.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        # Solo se pueden eliminar solicitudes en estado inicial
        if not self.object.estado.es_inicial:
            messages.warning(request, 'Solo se pueden eliminar solicitudes en estado inicial.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Solicitud {self.object.numero}'
        context['solicitud'] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        """Procesa la eliminación con log de auditoría."""
        self.object = self.get_object()
        numero = self.object.numero

        # Eliminar
        response = super().delete(request, *args, **kwargs)

        # Log de auditoría (usar número guardado)
        registrar_log_auditoria(
            usuario=request.user,
            accion_glosa='ELIMINAR',
            descripcion=f'Eliminó solicitud {numero}',
            request=request
        )

        messages.success(request, f'Solicitud {numero} eliminada exitosamente.')
        return response


# ==================== VISTAS DE WORKFLOW (APROBAR, RECHAZAR, DESPACHAR) ====================

class SolicitudAprobarView(BaseAuditedViewMixin, AtomicTransactionMixin, DetailView):
    """
    Vista para aprobar una solicitud.

    Permisos: solicitudes.aprobar_solicitud
    Auditoría: Registra acción APROBAR automáticamente
    Transacción atómica: Garantiza consistencia del workflow
    """
    model = Solicitud
    template_name = 'solicitudes/aprobar_solicitud.html'
    context_object_name = 'solicitud'
    permission_required = 'solicitudes.aprobar_solicitud'

    # Configuración de auditoría
    audit_action = 'APROBAR'
    audit_description_template = 'Aprobó solicitud {obj.numero}'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega formulario y datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Aprobar Solicitud {self.object.numero}'

        if self.request.POST:
            context['form'] = AprobarSolicitudForm(self.request.POST, solicitud=self.object)
        else:
            context['form'] = AprobarSolicitudForm(solicitud=self.object)

        return context

    def get(self, request, *args, **kwargs):
        """Verifica que la solicitud pueda ser aprobada."""
        self.object = self.get_object()

        # Verificar si la solicitud requiere aprobación
        if not self.object.tipo_solicitud.requiere_aprobacion:
            messages.warning(request, 'Esta solicitud no requiere aprobación.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        # Verificar que no esté ya aprobada
        if self.object.aprobador:
            messages.warning(request, 'Esta solicitud ya fue aprobada.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Procesa la aprobación de la solicitud usando SolicitudService."""
        self.object = self.get_object()
        form = AprobarSolicitudForm(request.POST, solicitud=self.object)

        if form.is_valid():
            solicitud_service = SolicitudService()

            # Preparar detalles aprobados
            detalles_aprobados = []
            for detalle in self.object.detalles.all():
                field_name = f'cantidad_aprobada_{detalle.id}'
                if field_name in form.cleaned_data:
                    detalles_aprobados.append({
                        'detalle_id': detalle.id,
                        'cantidad_aprobada': form.cleaned_data[field_name]
                    })

            try:
                # Aprobar usando service
                self.object = solicitud_service.aprobar_solicitud(
                    solicitud=self.object,
                    aprobador=request.user,
                    detalles_aprobados=detalles_aprobados,
                    notas_aprobacion=form.cleaned_data.get('notas_aprobacion', '')
                )

                # Log de auditoría
                self.log_action(self.object, request)

                messages.success(request, f'Solicitud {self.object.numero} aprobada exitosamente.')
                return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

            except ValidationError as e:
                error_msg = str(e.message_dict.get('__all__', [e])[0]) if hasattr(e, 'message_dict') else str(e)
                messages.error(request, error_msg)
                return self.render_to_response(self.get_context_data(form=form))

        # Si el formulario no es válido, mostrar errores
        return self.render_to_response(self.get_context_data(form=form))


class SolicitudRechazarView(BaseAuditedViewMixin, AtomicTransactionMixin, DetailView):
    """
    Vista para rechazar una solicitud.

    Permisos: solicitudes.rechazar_solicitud
    Auditoría: Registra acción RECHAZAR automáticamente
    Transacción atómica: Garantiza consistencia del workflow
    """
    model = Solicitud
    template_name = 'solicitudes/rechazar_solicitud.html'
    context_object_name = 'solicitud'
    permission_required = 'solicitudes.rechazar_solicitud'

    # Configuración de auditoría
    audit_action = 'RECHAZAR'
    audit_description_template = 'Rechazó solicitud {obj.numero}'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega formulario y datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Rechazar Solicitud {self.object.numero}'

        if self.request.POST:
            context['form'] = RechazarSolicitudForm(self.request.POST)
        else:
            context['form'] = RechazarSolicitudForm()

        return context

    def get(self, request, *args, **kwargs):
        """Verifica que la solicitud pueda ser rechazada."""
        self.object = self.get_object()

        # Verificar que no esté ya procesada
        if self.object.estado.es_final:
            messages.warning(request, 'Esta solicitud ya fue procesada.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Procesa el rechazo de la solicitud usando SolicitudService."""
        self.object = self.get_object()
        form = RechazarSolicitudForm(request.POST)

        if form.is_valid():
            solicitud_service = SolicitudService()

            try:
                # Rechazar usando service
                self.object = solicitud_service.rechazar_solicitud(
                    solicitud=self.object,
                    rechazador=request.user,
                    motivo_rechazo=form.cleaned_data['motivo_rechazo']
                )

                # Log de auditoría
                self.log_action(self.object, request)

                messages.success(request, f'Solicitud {self.object.numero} rechazada.')
                return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

            except ValidationError as e:
                error_msg = str(e.message_dict.get('__all__', [e])[0]) if hasattr(e, 'message_dict') else str(e)
                messages.error(request, error_msg)
                return self.render_to_response(self.get_context_data(form=form))

        # Si el formulario no es válido, mostrar errores
        return self.render_to_response(self.get_context_data(form=form))


class SolicitudDespacharView(BaseAuditedViewMixin, AtomicTransactionMixin, DetailView):
    """
    Vista para despachar una solicitud.

    Permisos: solicitudes.despachar_solicitud
    Auditoría: Registra acción DESPACHAR automáticamente
    Transacción atómica: Garantiza consistencia del workflow
    """
    model = Solicitud
    template_name = 'solicitudes/despachar_solicitud.html'
    context_object_name = 'solicitud'
    permission_required = 'solicitudes.despachar_solicitud'

    # Configuración de auditoría
    audit_action = 'DESPACHAR'
    audit_description_template = 'Despachó solicitud {obj.numero}'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega formulario y datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Despachar Solicitud {self.object.numero}'

        if self.request.POST:
            context['form'] = DespacharSolicitudForm(self.request.POST, solicitud=self.object)
        else:
            context['form'] = DespacharSolicitudForm(solicitud=self.object)

        return context

    def get(self, request, *args, **kwargs):
        """Verifica que la solicitud pueda ser despachada."""
        self.object = self.get_object()

        # Verificar que esté aprobada
        if not self.object.aprobador:
            messages.warning(request, 'Solo se pueden despachar solicitudes aprobadas.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        # Verificar que no esté ya despachada
        if self.object.despachador:
            messages.warning(request, 'Esta solicitud ya fue despachada.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Procesa el despacho de la solicitud usando SolicitudService."""
        self.object = self.get_object()
        form = DespacharSolicitudForm(request.POST, solicitud=self.object)

        if form.is_valid():
            solicitud_service = SolicitudService()

            # Preparar detalles despachados
            detalles_despachados = []
            for detalle in self.object.detalles.all():
                field_name = f'cantidad_despachada_{detalle.id}'
                if field_name in form.cleaned_data:
                    detalles_despachados.append({
                        'detalle_id': detalle.id,
                        'cantidad_despachada': form.cleaned_data[field_name]
                    })

            try:
                # Despachar usando service
                self.object = solicitud_service.despachar_solicitud(
                    solicitud=self.object,
                    despachador=request.user,
                    detalles_despachados=detalles_despachados,
                    notas_despacho=form.cleaned_data.get('notas_despacho', '')
                )

                # Log de auditoría
                self.log_action(self.object, request)

                messages.success(request, f'Solicitud {self.object.numero} despachada exitosamente.')
                return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

            except ValidationError as e:
                error_msg = str(e.message_dict.get('__all__', [e])[0]) if hasattr(e, 'message_dict') else str(e)
                messages.error(request, error_msg)
                return self.render_to_response(self.get_context_data(form=form))

        # Si el formulario no es válido, mostrar errores
        return self.render_to_response(self.get_context_data(form=form))


# ==================== VISTAS ESPECÍFICAS PARA ACTIVOS ====================

class SolicitudActivoListView(SolicitudListView):
    """Vista para listar solicitudes de activos/bienes."""
    template_name = 'solicitudes/lista_solicitudes_activos.html'

    def get_queryset(self) -> QuerySet:
        """Filtra solo solicitudes de activos."""
        return super().get_queryset().filter(tipo='ACTIVO')

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Solicitudes de Activos/Bienes'
        context['tipo'] = 'ACTIVO'
        return context


class SolicitudActivoCreateView(SolicitudCreateView):
    """Vista para crear una nueva solicitud de bienes."""
    template_name = 'solicitudes/form_solicitud.html'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto y formset de BIENES."""
        context = super(SolicitudCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Crear Solicitud de Bienes'
        context['action'] = 'Crear'
        context['tipo'] = 'ACTIVO'

        # Usar formset de BIENES/ACTIVOS
        if self.request.POST:
            context['formset'] = DetalleSolicitudActivoFormSet(self.request.POST)
        else:
            context['formset'] = DetalleSolicitudActivoFormSet()

        return context

    def form_valid(self, form):
        """Procesa el formulario válido usando SolicitudService con tipo ACTIVO."""
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            solicitud_service = SolicitudService()

            try:
                # Crear solicitud usando service con tipo ACTIVO
                self.object = solicitud_service.crear_solicitud(
                    tipo_solicitud=form.cleaned_data['tipo_solicitud'],
                    solicitante=self.request.user,
                    fecha_requerida=form.cleaned_data['fecha_requerida'],
                    motivo=form.cleaned_data['motivo'],
                    area_solicitante=form.cleaned_data['area_solicitante'],
                    titulo_actividad=form.cleaned_data.get('titulo_actividad', ''),
                    objetivo_actividad=form.cleaned_data.get('objetivo_actividad', ''),
                    tipo_choice='ACTIVO',  # FORZAR TIPO ACTIVO
                    bodega_origen=None,  # Los bienes no tienen bodega
                    departamento=form.cleaned_data.get('departamento'),
                    area=form.cleaned_data.get('area'),
                    equipo=form.cleaned_data.get('equipo'),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )

                # Guardar los detalles
                formset.instance = self.object
                formset.save()

                # Mensaje de éxito y log de auditoría
                messages.success(self.request, self.get_success_message(self.object))
                self.log_action(self.object, self.request)

                return redirect(self.get_success_url())

            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class SolicitudActivoUpdateView(SolicitudUpdateView):
    """Vista para editar una solicitud de bienes."""
    template_name = 'solicitudes/form_solicitud.html'

    def get_queryset(self) -> QuerySet:
        """Solo solicitudes de bienes."""
        return super().get_queryset().filter(tipo='ACTIVO')

    def get(self, request, *args, **kwargs):
        """Verifica que la solicitud pueda ser editada."""
        self.object = self.get_object()

        # Solo se pueden editar si están en estado pendiente o rechazada
        if self.object.estado.codigo not in ['PENDIENTE', 'RECHAZADA']:
            messages.error(request, 'Solo se pueden editar solicitudes en estado Pendiente o Rechazada.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto y formset de BIENES."""
        context = super(SolicitudUpdateView, self).get_context_data(**kwargs)
        context['titulo'] = f'Editar Solicitud de Bienes {self.object.numero}'
        context['action'] = 'Editar'
        context['tipo'] = 'ACTIVO'
        context['solicitud'] = self.object

        # Usar formset de BIENES/ACTIVOS
        if self.request.POST:
            context['formset'] = DetalleSolicitudActivoFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DetalleSolicitudActivoFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        """Asegura que no tenga bodega."""
        form.instance.bodega_origen = None
        return super().form_valid(form)


# ==================== VISTAS ESPECÍFICAS PARA ARTÍCULOS ====================

class SolicitudArticuloListView(SolicitudListView):
    """Vista para listar solicitudes de artículos."""
    template_name = 'solicitudes/lista_solicitudes_articulos.html'

    def get_queryset(self) -> QuerySet:
        """Filtra solo solicitudes de artículos."""
        return super().get_queryset().filter(tipo='ARTICULO')

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Solicitudes de Artículos'
        context['tipo'] = 'ARTICULO'
        return context


class SolicitudArticuloCreateView(SolicitudCreateView):
    """Vista para crear una nueva solicitud de artículos."""
    template_name = 'solicitudes/form_solicitud.html'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto y formset de ARTÍCULOS."""
        context = super(SolicitudCreateView, self).get_context_data(**kwargs)
        context['titulo'] = 'Crear Solicitud de Artículos'
        context['action'] = 'Crear'
        context['tipo'] = 'ARTICULO'

        # Usar formset de ARTÍCULOS
        if self.request.POST:
            context['formset'] = DetalleSolicitudArticuloFormSet(self.request.POST)
        else:
            context['formset'] = DetalleSolicitudArticuloFormSet()

        return context

    def form_valid(self, form):
        """Procesa el formulario válido usando SolicitudService con tipo ARTICULO."""
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            solicitud_service = SolicitudService()

            try:
                # Crear solicitud usando service con tipo ARTICULO
                self.object = solicitud_service.crear_solicitud(
                    tipo_solicitud=form.cleaned_data['tipo_solicitud'],
                    solicitante=self.request.user,
                    fecha_requerida=form.cleaned_data['fecha_requerida'],
                    motivo=form.cleaned_data['motivo'],
                    area_solicitante=form.cleaned_data['area_solicitante'],
                    titulo_actividad=form.cleaned_data.get('titulo_actividad', ''),
                    objetivo_actividad=form.cleaned_data.get('objetivo_actividad', ''),
                    tipo_choice='ARTICULO',  # FORZAR TIPO ARTICULO
                    bodega_origen=form.cleaned_data.get('bodega_origen'),
                    departamento=form.cleaned_data.get('departamento'),
                    area=form.cleaned_data.get('area'),
                    equipo=form.cleaned_data.get('equipo'),
                    observaciones=form.cleaned_data.get('observaciones', '')
                )

                # Guardar los detalles
                formset.instance = self.object
                formset.save()

                # Mensaje de éxito y log de auditoría
                messages.success(self.request, self.get_success_message(self.object))
                self.log_action(self.object, self.request)

                return redirect(self.get_success_url())

            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class SolicitudArticuloUpdateView(SolicitudUpdateView):
    """Vista para editar una solicitud de artículos."""
    template_name = 'solicitudes/form_solicitud.html'

    def get_queryset(self) -> QuerySet:
        """Solo solicitudes de artículos."""
        return super().get_queryset().filter(tipo='ARTICULO')

    def get(self, request, *args, **kwargs):
        """Verifica que la solicitud pueda ser editada."""
        self.object = self.get_object()

        # Solo se pueden editar si están en estado pendiente o rechazada
        if self.object.estado.codigo not in ['PENDIENTE', 'RECHAZADA']:
            messages.error(request, 'Solo se pueden editar solicitudes en estado Pendiente o Rechazada.')
            return redirect('solicitudes:detalle_solicitud', pk=self.object.pk)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto y formset de ARTÍCULOS."""
        context = super(SolicitudUpdateView, self).get_context_data(**kwargs)
        context['titulo'] = f'Editar Solicitud de Artículos {self.object.numero}'
        context['action'] = 'Editar'
        context['tipo'] = 'ARTICULO'
        context['solicitud'] = self.object

        # Usar formset de ARTÍCULOS
        if self.request.POST:
            context['formset'] = DetalleSolicitudArticuloFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DetalleSolicitudArticuloFormSet(instance=self.object)

        return context
