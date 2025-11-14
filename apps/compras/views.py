"""
Class-Based Views para el módulo de compras.

Este archivo implementa todas las vistas usando CBVs siguiendo SOLID y DRY:
- Reutilización de mixins de core.mixins
- Separación de responsabilidades (Repository Pattern + Service Layer)
- Código limpio y mantenible
- Type hints completos
- Auditoría automática
"""
from typing import Any
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from decimal import Decimal
from core.mixins import (
    BaseAuditedViewMixin, AtomicTransactionMixin, SoftDeleteMixin,
    PaginatedListMixin, FilteredListMixin
)
from .models import (
    Proveedor, OrdenCompra, DetalleOrdenCompraArticulo, DetalleOrdenCompra,
    EstadoOrdenCompra, RecepcionArticulo, DetalleRecepcionArticulo,
    EstadoRecepcion, TipoRecepcion, RecepcionActivo, DetalleRecepcionActivo
)
from .forms import (
    ProveedorForm, OrdenCompraForm, DetalleOrdenCompraArticuloForm,
    DetalleOrdenCompraActivoForm, OrdenCompraFiltroForm,
    RecepcionArticuloForm, DetalleRecepcionArticuloForm, RecepcionArticuloFiltroForm,
    RecepcionActivoForm, DetalleRecepcionActivoForm, RecepcionActivoFiltroForm
)
from .repositories import (
    ProveedorRepository, OrdenCompraRepository, EstadoOrdenCompraRepository,
    RecepcionArticuloRepository, RecepcionActivoRepository, EstadoRecepcionRepository
)
from .services import (
    ProveedorService, OrdenCompraService,
    RecepcionArticuloService, RecepcionActivoService
)
from apps.bodega.models import Bodega, Articulo, Movimiento, TipoMovimiento


# ==================== MIXINS GENÉRICOS PARA RECEPCIONES (DRY) ====================

class RecepcionListMixin:
    """
    Mixin genérico para vistas de listado de recepciones.

    Proporciona funcionalidad común para listar recepciones con filtros.
    Las subclases deben definir:
    - model: Modelo de recepción (RecepcionArticulo o RecepcionActivo)
    - repository_class: Clase del repository
    - filter_form_class: Formulario de filtros
    - titulo: Título de la página
    """
    repository_class = None
    titulo = "Recepciones"

    def get_queryset(self) -> QuerySet:
        """
        Retorna recepciones con filtros aplicados.

        Hook method _aplicar_filtros_especificos() permite filtros adicionales.
        """
        if not self.repository_class:
            return super().get_queryset()

        repo = self.repository_class()
        queryset = repo.get_all()

        # Aplicar filtros del formulario
        form = self.filter_form_class(self.request.GET)
        if form.is_valid():
            queryset = self._aplicar_filtros(queryset, form.cleaned_data, repo)

        return queryset.order_by('-fecha_recepcion')

    def _aplicar_filtros(self, queryset, data, repo):
        """
        Aplica filtros comunes (estado) y específicos.

        Args:
            queryset: QuerySet base
            data: Datos limpios del formulario
            repo: Repository de recepción

        Returns:
            QuerySet filtrado
        """
        # Filtro común: estado
        if data.get('estado'):
            estado_repo = EstadoRecepcionRepository()
            estado = estado_repo.get_by_id(data['estado'].id)
            if estado:
                queryset = repo.filter_by_estado(estado)

        # Hook para filtros específicos (ej: bodega)
        queryset = self._aplicar_filtros_especificos(queryset, data, repo)

        return queryset

    def _aplicar_filtros_especificos(self, queryset, data, repo):
        """Hook method para filtros específicos de subclases."""
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        context['form'] = self.filter_form_class(self.request.GET)
        return context


class RecepcionDetailMixin:
    """
    Mixin genérico para vistas de detalle de recepciones.

    Proporciona funcionalidad común para mostrar detalle de recepciones.
    """

    def get_queryset(self) -> QuerySet:
        """Optimiza consultas y filtra no eliminados."""
        queryset = super().get_queryset().filter(eliminado=False)
        return self._optimize_queryset(queryset)

    def _optimize_queryset(self, queryset):
        """Hook method para optimizar consultas específicas."""
        base_related = ['orden_compra', 'estado', 'recibido_por']

        # Verificar si el modelo tiene bodega
        if hasattr(self.model, '_meta') and 'bodega' in [f.name for f in self.model._meta.get_fields()]:
            base_related.append('bodega')

        return queryset.select_related(*base_related)

    def get_context_data(self, **kwargs) -> dict:
        """Agrega detalles al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Recepción {self.object.numero}'

        # Obtener detalles con optimización
        detalles_queryset = self.object.detalles.filter(eliminado=False)
        context['detalles'] = self._optimize_detalles_queryset(detalles_queryset)

        return context

    def _optimize_detalles_queryset(self, queryset):
        """Hook method para optimizar consultas de detalles."""
        return queryset


class RecepcionAgregarMixin:
    """
    Mixin genérico para agregar items a una recepción.

    Las subclases deben definir:
    - service_class: Clase del service
    - repository_class: Clase del repository
    - item_field_name: Nombre del campo del item ('articulo' o 'activo')
    - success_message: Mensaje de éxito
    """
    service_class = None
    repository_class = None
    item_field_name = None
    detail_url_name = None

    def get_success_url(self) -> str:
        """Redirige al detalle de la recepción."""
        return reverse_lazy(self.detail_url_name, kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        repo = self.repository_class()
        context['recepcion'] = repo.get_by_id(self.kwargs['pk'])
        context['titulo'] = self.get_titulo()
        context['action'] = 'Agregar'
        return context

    def get_titulo(self):
        """Hook method para título personalizado."""
        return 'Agregar Item a Recepción'

    def form_valid(self, form):
        """Procesa el formulario usando service."""
        repo = self.repository_class()
        recepcion = repo.get_by_id(self.kwargs['pk'])

        if not recepcion:
            messages.error(self.request, 'Recepción no encontrada.')
            return redirect(self.get_lista_url())

        service = self.service_class()

        try:
            # Preparar argumentos para service
            item = form.cleaned_data[self.item_field_name]
            cantidad = form.cleaned_data['cantidad']
            kwargs = self._preparar_kwargs_detalle(form)

            # Agregar detalle usando service
            # Construir argumentos con el nombre correcto del campo
            detalle_kwargs = {
                'recepcion': recepcion,
                self.item_field_name: item,
                'cantidad': cantidad,
                **kwargs
            }
            self.object = service.agregar_detalle(**detalle_kwargs)

            messages.success(self.request, self.success_message)

            # Log de auditoría
            self.audit_description_template = self._get_audit_description(recepcion)
            self.log_action(self.object, self.request)

            return redirect(self.get_success_url())

        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field if field != '__all__' else None, error)
            return self.form_invalid(form)

    def _preparar_kwargs_detalle(self, form):
        """Hook method para preparar argumentos específicos."""
        return {
            'observaciones': form.cleaned_data.get('observaciones', '')
        }

    def _get_audit_description(self, recepcion):
        """Hook method para descripción de auditoría."""
        return f'Agregó item a recepción {recepcion.numero}'

    def get_lista_url(self):
        """Hook method para URL de lista."""
        raise NotImplementedError("Subclases deben implementar get_lista_url()")


class RecepcionConfirmarMixin:
    """
    Mixin genérico para confirmar recepciones.

    Maneja cambio de estado y permite hook para acciones específicas
    como actualización de stock (solo artículos).
    """

    def get_queryset(self) -> QuerySet:
        """Solo recepciones no eliminadas."""
        return super().get_queryset().filter(eliminado=False)

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Confirmar Recepción'
        return context

    def post(self, request, *args, **kwargs):
        """Procesa la confirmación de la recepción."""
        self.object = self.get_object()

        # Cambiar estado a completada
        estado_repo = EstadoRecepcionRepository()
        estado_completado = estado_repo.get_by_codigo('COMPLETADA')

        if not estado_completado:
            # Si no existe COMPLETADA, buscar cualquier estado final excluyendo CANCELADA
            estado_completado = EstadoRecepcion.objects.filter(
                es_final=True, activo=True, eliminado=False
            ).exclude(codigo='CANCELADA').first()

        if estado_completado:
            self.object.estado = estado_completado
            self.object.save()

        # Hook para acciones específicas (ej: actualizar stock)
        self._post_confirmar_acciones(request)

        # Log de auditoría
        self.log_action(self.object, request)

        messages.success(request, self.get_success_message())
        return redirect(self.get_success_url_after_confirm())

    def _post_confirmar_acciones(self, request):
        """
        Hook method para acciones después de confirmar.

        Ejemplo: actualizar stock para artículos.
        """
        pass

    def get_success_message(self):
        """Hook method para mensaje de éxito."""
        return 'Recepción confirmada exitosamente.'

    def get_success_url_after_confirm(self):
        """Hook method para URL después de confirmar."""
        raise NotImplementedError("Subclases deben implementar get_success_url_after_confirm()")


# ==================== VISTA MENÚ PRINCIPAL ====================

class MenuComprasView(BaseAuditedViewMixin, TemplateView):
    """
    Vista del menú principal del módulo de compras.

    Muestra estadísticas y accesos rápidos basados en permisos del usuario.
    Permisos: compras.view_ordencompra
    Utiliza: Repositories para acceso a datos optimizado
    """
    template_name = 'compras/menu_compras.html'
    permission_required = 'compras.view_ordencompra'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega estadísticas y permisos al contexto usando repositories."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Inicializar repositories
        orden_repo = OrdenCompraRepository()
        proveedor_repo = ProveedorRepository()
        recepcion_articulo_repo = RecepcionArticuloRepository()
        recepcion_activo_repo = RecepcionActivoRepository()
        estado_repo = EstadoOrdenCompraRepository()

        # Estadísticas del módulo usando repositories
        estado_pendiente = estado_repo.get_by_codigo('PENDIENTE')
        ordenes_pendientes_count = 0
        if estado_pendiente:
            ordenes_pendientes_count = orden_repo.filter_by_estado(estado_pendiente).count()

        context['stats'] = {
            'total_ordenes': orden_repo.get_all().count(),
            'ordenes_pendientes': ordenes_pendientes_count,
            'recepciones_articulos': recepcion_articulo_repo.get_all().count(),
            'recepciones_activos': recepcion_activo_repo.get_all().count(),
            'proveedores_activos': proveedor_repo.get_active().count(),
        }

        # Permisos del usuario
        context['permisos'] = {
            'puede_crear': user.has_perm('compras.add_ordencompra'),
            'puede_recepcionar': user.has_perm('compras.add_recepcionarticulo') or user.has_perm('compras.add_recepcionactivo'),
            'puede_gestionar': user.has_perm('compras.change_ordencompra'),
        }

        context['titulo'] = 'Módulo de Compras'
        return context


# ==================== VISTAS DE PROVEEDORES ====================

class ProveedorListView(BaseAuditedViewMixin, PaginatedListMixin, ListView):
    """
    Vista para listar proveedores.

    Permisos: compras.view_proveedor
    Utiliza: ProveedorRepository para acceso a datos
    """
    model = Proveedor
    template_name = 'compras/proveedor/lista.html'
    context_object_name = 'proveedores'
    permission_required = 'compras.view_proveedor'
    paginate_by = 25

    def get_queryset(self) -> QuerySet:
        """Retorna proveedores usando repository."""
        proveedor_repo = ProveedorRepository()

        # Búsqueda por query string
        query = self.request.GET.get('q', '').strip()
        if query:
            return proveedor_repo.search(query)

        return proveedor_repo.get_all()

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Proveedores'
        return context


class ProveedorCreateView(BaseAuditedViewMixin, CreateView):
    """
    Vista para crear un nuevo proveedor.

    Permisos: compras.add_proveedor
    Auditoría: Registra acción CREAR automáticamente
    """
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'compras/proveedor/form.html'
    permission_required = 'compras.add_proveedor'
    success_url = reverse_lazy('compras:proveedor_lista')

    # Configuración de auditoría
    audit_action = 'CREAR'
    audit_description_template = 'Creó proveedor {obj.rut} - {obj.razon_social}'

    # Mensaje de éxito
    success_message = 'Proveedor {obj.razon_social} creado exitosamente.'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Proveedor'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form):
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class ProveedorUpdateView(BaseAuditedViewMixin, UpdateView):
    """
    Vista para editar un proveedor existente.

    Permisos: compras.change_proveedor
    Auditoría: Registra acción EDITAR automáticamente
    """
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'compras/proveedor/form.html'
    permission_required = 'compras.change_proveedor'
    success_url = reverse_lazy('compras:proveedor_lista')

    # Configuración de auditoría
    audit_action = 'EDITAR'
    audit_description_template = 'Editó proveedor {obj.rut} - {obj.razon_social}'

    # Mensaje de éxito
    success_message = 'Proveedor {obj.razon_social} actualizado exitosamente.'

    def get_queryset(self) -> QuerySet:
        """Solo permite editar proveedores no eliminados."""
        return super().get_queryset().filter(eliminado=False)

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Proveedor {self.object.razon_social}'
        context['action'] = 'Actualizar'
        context['proveedor'] = self.object
        return context

    def form_valid(self, form):
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class ProveedorDeleteView(BaseAuditedViewMixin, DeleteView):
    """
    Vista para eliminar (soft delete) un proveedor.

    Permisos: compras.delete_proveedor
    Auditoría: Registra acción ELIMINAR automáticamente
    Utiliza: ProveedorService para validaciones y eliminación
    """
    model = Proveedor
    template_name = 'compras/proveedor/eliminar.html'
    permission_required = 'compras.delete_proveedor'
    success_url = reverse_lazy('compras:proveedor_lista')

    # Configuración de auditoría
    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó proveedor {obj.rut} - {obj.razon_social}'

    # Mensaje de éxito
    success_message = 'Proveedor {obj.razon_social} eliminado exitosamente.'

    def get_queryset(self) -> QuerySet:
        """Solo permite eliminar proveedores no eliminados."""
        proveedor_repo = ProveedorRepository()
        return proveedor_repo.get_all()

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Proveedor {self.object.razon_social}'
        context['proveedor'] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        """Elimina usando service con validaciones."""
        self.object = self.get_object()
        proveedor_service = ProveedorService()

        try:
            proveedor_service.eliminar_proveedor(self.object)
            messages.success(request, self.get_success_message(self.object))
            self.log_action(self.object, request)
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(request, str(e.message_dict.get('__all__', [e])[0]))
            return redirect('compras:proveedor_lista')


# ==================== VISTAS DE ÓRDENES DE COMPRA ====================

class OrdenCompraListView(BaseAuditedViewMixin, PaginatedListMixin, FilteredListMixin, ListView):
    """
    Vista para listar órdenes de compra con filtros.

    Permisos: compras.view_ordencompra
    Filtros: Estado, proveedor, búsqueda por número
    Utiliza: OrdenCompraRepository para acceso a datos optimizado
    """
    model = OrdenCompra
    template_name = 'compras/orden/lista.html'
    context_object_name = 'ordenes'
    permission_required = 'compras.view_ordencompra'
    paginate_by = 25
    filter_form_class = OrdenCompraFiltroForm

    def get_queryset(self) -> QuerySet:
        """Retorna órdenes usando repository con filtros."""
        orden_repo = OrdenCompraRepository()
        queryset = orden_repo.get_all()

        # Aplicar filtros del formulario
        form = self.filter_form_class(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data

            # Filtro de búsqueda
            if data.get('q'):
                queryset = orden_repo.search(data['q'])

            # Filtro por estado
            if data.get('estado'):
                queryset = queryset.filter(estado=data['estado'])

            # Filtro por proveedor
            if data.get('proveedor'):
                queryset = queryset.filter(proveedor=data['proveedor'])

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Órdenes de Compra'
        context['form'] = self.filter_form_class(self.request.GET)
        return context


class OrdenCompraDetailView(BaseAuditedViewMixin, DetailView):
    """
    Vista para ver el detalle de una orden de compra.

    Permisos: compras.view_ordencompra
    """
    model = OrdenCompra
    template_name = 'compras/orden/detalle.html'
    context_object_name = 'orden'
    permission_required = 'compras.view_ordencompra'

    def get_queryset(self) -> QuerySet:
        """Optimiza consultas con select_related."""
        return super().get_queryset().select_related(
            'proveedor', 'estado', 'solicitante', 'aprobador', 'bodega_destino'
        )

    def get_context_data(self, **kwargs) -> dict:
        """Agrega detalles al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Orden de Compra {self.object.numero}'

        # Detalles de artículos
        context['detalles_articulos'] = self.object.detalles_articulos.filter(
            eliminado=False
        ).select_related('articulo', 'articulo__categoria')

        # Detalles de activos
        context['detalles_activos'] = self.object.detalles.filter(
            eliminado=False
        ).select_related('activo')

        return context


class OrdenCompraCreateView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para crear una nueva orden de compra.

    Permisos: compras.add_ordencompra
    Auditoría: Registra acción CREAR automáticamente
    Transacción atómica: Garantiza que el número se genere correctamente
    """
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'compras/orden/form.html'
    permission_required = 'compras.add_ordencompra'

    # Configuración de auditoría
    audit_action = 'CREAR'
    audit_description_template = 'Creó orden de compra {obj.numero}'

    # Mensaje de éxito
    success_message = 'Orden de compra {obj.numero} creada exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la orden creada."""
        return reverse_lazy('compras:orden_compra_detalle', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Orden de Compra'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form):
        """Procesa el formulario válido con log de auditoría y genera número automático."""
        from decimal import Decimal
        from core.utils.business import generar_codigo_con_anio
        from apps.solicitudes.models import DetalleSolicitud

        # Asignar solicitante
        form.instance.solicitante = self.request.user

        # Generar número de orden automáticamente con año
        form.instance.numero = generar_codigo_con_anio('OC', OrdenCompra, 'numero', longitud=6)

        response = super().form_valid(form)

        # Agregar automáticamente los detalles de las solicitudes asociadas
        solicitudes = form.cleaned_data.get('solicitudes', [])
        if solicitudes:
            for solicitud in solicitudes:
                # Obtener detalles aprobados de la solicitud
                detalles = solicitud.detalles.filter(cantidad_aprobada__gt=0)

                for detalle in detalles:
                    if detalle.articulo:
                        # Crear detalle de orden para artículo
                        # Los artículos no tienen precio_unitario, usar 0
                        DetalleOrdenCompraArticulo.objects.create(
                            orden_compra=self.object,
                            articulo=detalle.articulo,
                            cantidad=detalle.cantidad_aprobada,
                            precio_unitario=Decimal('0'),
                            descuento=Decimal('0')
                        )
                    elif detalle.activo:
                        # Crear detalle de orden para activo
                        # Obtener precio del activo o usar 0 si es None
                        precio = getattr(detalle.activo, 'precio_unitario', None) or Decimal('0')
                        DetalleOrdenCompra.objects.create(
                            orden_compra=self.object,
                            activo=detalle.activo,
                            cantidad=detalle.cantidad_aprobada,
                            precio_unitario=precio,
                            descuento=Decimal('0')
                        )

            # Recalcular totales de la orden
            orden_service = OrdenCompraService()
            orden_service.recalcular_totales(self.object)

        self.log_action(self.object, self.request)
        return response


class OrdenCompraUpdateView(BaseAuditedViewMixin, UpdateView):
    """
    Vista para editar una orden de compra existente.

    Permisos: compras.change_ordencompra
    Auditoría: Registra acción EDITAR automáticamente
    """
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'compras/orden/form.html'
    permission_required = 'compras.change_ordencompra'

    # Configuración de auditoría
    audit_action = 'EDITAR'
    audit_description_template = 'Editó orden de compra {obj.numero}'

    # Mensaje de éxito
    success_message = 'Orden de compra {obj.numero} actualizada exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la orden editada."""
        return reverse_lazy('compras:orden_compra_detalle', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Orden de Compra {self.object.numero}'
        context['action'] = 'Actualizar'
        context['orden'] = self.object
        return context

    def form_valid(self, form):
        """Procesa el formulario válido con log de auditoría."""
        response = super().form_valid(form)
        self.log_action(self.object, self.request)
        return response


class OrdenCompraDeleteView(BaseAuditedViewMixin, DeleteView):
    """
    Vista para eliminar una orden de compra (soft delete de detalles).

    Permisos: compras.delete_ordencompra
    Auditoría: Registra acción ELIMINAR automáticamente
    """
    model = OrdenCompra
    template_name = 'compras/orden/eliminar.html'
    permission_required = 'compras.delete_ordencompra'
    success_url = reverse_lazy('compras:orden_compra_lista')

    # Configuración de auditoría
    audit_action = 'ELIMINAR'
    audit_description_template = 'Eliminó orden de compra {obj.numero}'

    # Mensaje de éxito
    success_message = 'Orden de compra {obj.numero} eliminada exitosamente.'

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar Orden de Compra {self.object.numero}'
        context['orden'] = self.object
        # Verificar si puede eliminar
        context['es_final'] = self.object.estado.es_final if self.object.estado else False
        return context

    def delete(self, request, *args, **kwargs):
        """Sobrescribe delete para hacer soft delete de detalles."""
        self.object = self.get_object()

        # Verificar que se pueda eliminar
        if self.object.estado and self.object.estado.es_final:
            messages.error(request, 'No se puede eliminar una orden en estado final.')
            return redirect('compras:orden_compra_lista')

        # Soft delete de los detalles
        self.object.detalles_articulos.update(eliminado=True, activo=False)
        self.object.detalles.update(eliminado=True, activo=False)

        # Log de auditoría
        if hasattr(self, 'log_action'):
            self.log_action(self.object, request)

        messages.success(request, self.get_success_message(self.object))
        return redirect(self.success_url)


class ObtenerDetallesSolicitudesView(View):
    """
    Vista AJAX para obtener los detalles de solicitudes seleccionadas.
    Retorna JSON con los artículos/activos de las solicitudes.
    """

    def get(self, request, *args, **kwargs):
        """Retorna los detalles de las solicitudes en formato JSON."""
        from django.http import JsonResponse
        from apps.solicitudes.models import Solicitud

        solicitud_ids = request.GET.getlist('solicitudes[]')

        if not solicitud_ids:
            return JsonResponse({'detalles': []})

        detalles_data = []

        for solicitud_id in solicitud_ids:
            try:
                solicitud = Solicitud.objects.get(id=solicitud_id, eliminado=False)
                detalles = solicitud.detalles.filter(cantidad_aprobada__gt=0)

                for detalle in detalles:
                    detalle_info = {
                        'solicitud_numero': solicitud.numero,
                        'tipo': 'articulo' if detalle.articulo else 'activo',
                        'codigo': detalle.producto_codigo,
                        'nombre': detalle.producto_nombre,
                        'cantidad_aprobada': str(detalle.cantidad_aprobada),
                    }

                    if detalle.articulo:
                        # Obtener unidades de medida concatenadas
                        unidades = detalle.articulo.unidades_medida.all()
                        detalle_info['unidad_medida'] = ', '.join([u.simbolo for u in unidades]) if unidades.exists() else 'unidad'
                        detalle_info['precio_unitario'] = str(detalle.articulo.precio_unitario if hasattr(detalle.articulo, 'precio_unitario') else 0)
                    else:
                        # Los activos son bienes únicos sin unidad de medida
                        detalle_info['unidad_medida'] = 'unidad'
                        detalle_info['precio_unitario'] = str(detalle.activo.precio_unitario if hasattr(detalle.activo, 'precio_unitario') else 0)

                    detalles_data.append(detalle_info)

            except Solicitud.DoesNotExist:
                continue

        return JsonResponse({'detalles': detalles_data})


class ObtenerArticulosOrdenCompraView(View):
    """
    Vista AJAX para obtener los artículos de una orden de compra.
    Retorna JSON con los artículos de la orden seleccionada.
    """

    def get(self, request, *args, **kwargs):
        """Retorna los artículos de la orden de compra en formato JSON."""
        from django.http import JsonResponse

        orden_id = request.GET.get('orden_id')

        if not orden_id:
            return JsonResponse({'articulos': []})

        try:
            orden = OrdenCompra.objects.get(id=orden_id)
            articulos_data = []

            # Obtener artículos de bodega
            detalles_articulos = orden.detalles_articulos.all().select_related('articulo')
            for detalle in detalles_articulos:
                # Obtener unidades de medida concatenadas
                unidades = detalle.articulo.unidades_medida.all()
                unidades_str = ', '.join([u.simbolo for u in unidades]) if unidades.exists() else 'unidad'

                articulos_data.append({
                    'id': detalle.articulo.id,
                    'sku': detalle.articulo.codigo,
                    'codigo': detalle.articulo.codigo,
                    'nombre': detalle.articulo.nombre,
                    'cantidad': str(detalle.cantidad),
                    'unidad_medida': unidades_str,
                    'tipo': 'articulo'
                })

            # Obtener activos (los activos no tienen unidad_medida, son bienes únicos)
            detalles_activos = orden.detalles.all().select_related('activo')
            for detalle in detalles_activos:
                articulos_data.append({
                    'id': detalle.activo.id,
                    'sku': detalle.activo.codigo,
                    'codigo': detalle.activo.codigo,
                    'nombre': detalle.activo.nombre,
                    'cantidad': str(detalle.cantidad),
                    'unidad_medida': 'unidad',  # Activos son bienes únicos sin unidad de medida
                    'tipo': 'activo'
                })

            return JsonResponse({'articulos': articulos_data})

        except OrdenCompra.DoesNotExist:
            return JsonResponse({'articulos': [], 'error': 'Orden de compra no encontrada'}, status=404)


class ObtenerActivosOrdenCompraView(View):
    """
    Vista AJAX para obtener los activos de una orden de compra.
    Retorna JSON con los activos de la orden seleccionada.
    """

    def get(self, request, *args, **kwargs):
        """Retorna los activos de la orden de compra en formato JSON."""
        from django.http import JsonResponse

        orden_id = request.GET.get('orden_id')

        if not orden_id:
            return JsonResponse({'activos': []})

        try:
            orden = OrdenCompra.objects.get(id=orden_id)
            activos_data = []

            # Obtener solo activos (no artículos)
            detalles_activos = orden.detalles.filter(eliminado=False).select_related('activo', 'activo__categoria')
            for detalle in detalles_activos:
                activos_data.append({
                    'id': detalle.activo.id,
                    'codigo': detalle.activo.codigo,
                    'nombre': detalle.activo.nombre,
                    'cantidad': str(detalle.cantidad),
                    'requiere_serie': detalle.activo.requiere_serie,
                    'categoria': detalle.activo.categoria.nombre if detalle.activo.categoria else ''
                })

            return JsonResponse({'activos': activos_data})

        except OrdenCompra.DoesNotExist:
            return JsonResponse({'activos': [], 'error': 'Orden de compra no encontrada'}, status=404)


class OrdenCompraAgregarArticuloView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para agregar un artículo a una orden de compra.

    Permisos: compras.add_detalleordencompraarticulo
    Auditoría: Registra acción CREAR automáticamente
    Transacción atómica: Garantiza que se actualicen los totales correctamente
    Utiliza: OrdenCompraService para recalcular totales
    """
    model = DetalleOrdenCompraArticulo
    form_class = DetalleOrdenCompraArticuloForm
    template_name = 'compras/orden/agregar_articulo.html'
    permission_required = 'compras.add_detalleordencompraarticulo'

    # Configuración de auditoría
    audit_action = 'CREAR'
    success_message = 'Artículo agregado exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la orden."""
        return reverse_lazy('compras:orden_compra_detalle', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        orden_repo = OrdenCompraRepository()
        orden = orden_repo.get_by_id(self.kwargs['pk'])
        context['orden'] = orden
        context['titulo'] = 'Agregar Artículo'
        context['action'] = 'Agregar'
        return context

    def form_valid(self, form):
        """Procesa el formulario y actualiza totales usando service."""
        orden_repo = OrdenCompraRepository()
        orden = orden_repo.get_by_id(self.kwargs['pk'])
        form.instance.orden_compra = orden
        response = super().form_valid(form)

        # Recalcular totales usando service
        orden_service = OrdenCompraService()
        orden_service.recalcular_totales(orden)

        # Log de auditoría
        self.audit_description_template = f'Agregó artículo {self.object.articulo.codigo} a orden {orden.numero}'
        self.log_action(self.object, self.request)

        return response


class OrdenCompraAgregarActivoView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para agregar un activo/bien a una orden de compra.

    Permisos: compras.add_detalleordencompra
    Auditoría: Registra acción CREAR automáticamente
    Transacción atómica: Garantiza que se actualicen los totales correctamente
    Utiliza: OrdenCompraService para recalcular totales
    """
    model = DetalleOrdenCompra
    form_class = DetalleOrdenCompraActivoForm
    template_name = 'compras/orden/agregar_activo.html'
    permission_required = 'compras.add_detalleordencompra'

    # Configuración de auditoría
    audit_action = 'CREAR'
    success_message = 'Activo agregado exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la orden."""
        return reverse_lazy('compras:orden_compra_detalle', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        context = super().get_context_data(**kwargs)
        orden_repo = OrdenCompraRepository()
        orden = orden_repo.get_by_id(self.kwargs['pk'])
        context['orden'] = orden
        context['titulo'] = 'Agregar Activo/Bien'
        context['action'] = 'Agregar'
        return context

    def form_valid(self, form):
        """Procesa el formulario y actualiza totales usando service."""
        orden_repo = OrdenCompraRepository()
        orden = orden_repo.get_by_id(self.kwargs['pk'])
        form.instance.orden_compra = orden
        response = super().form_valid(form)

        # Recalcular totales usando service
        orden_service = OrdenCompraService()
        orden_service.recalcular_totales(orden)

        # Log de auditoría
        self.audit_description_template = f'Agregó activo {self.object.activo.codigo} a orden {orden.numero}'
        self.log_action(self.object, self.request)

        return response


# ==================== VISTAS DE RECEPCIÓN DE ARTÍCULOS ====================

class RecepcionArticuloListView(RecepcionListMixin, BaseAuditedViewMixin, PaginatedListMixin, FilteredListMixin, ListView):
    """
    Vista para listar recepciones de artículos.

    Permisos: compras.view_recepcionarticulo
    Filtros: Estado, bodega
    Utiliza: RecepcionArticuloRepository y RecepcionListMixin (DRY)
    """
    model = RecepcionArticulo
    template_name = 'compras/recepcion_articulo/lista.html'
    context_object_name = 'recepciones'
    permission_required = 'compras.view_recepcionarticulo'
    paginate_by = 25
    filter_form_class = RecepcionArticuloFiltroForm
    repository_class = RecepcionArticuloRepository
    titulo = 'Recepciones de Artículos'

    def _aplicar_filtros_especificos(self, queryset, data, repo):
        """Aplica filtro específico de bodega para artículos."""
        if data.get('bodega'):
            from apps.bodega.repositories import BodegaRepository
            bodega_repo = BodegaRepository()
            bodega = bodega_repo.get_by_id(data['bodega'].id)
            if bodega:
                queryset = repo.filter_by_bodega(bodega)
        return queryset


class RecepcionArticuloDetailView(RecepcionDetailMixin, BaseAuditedViewMixin, DetailView):
    """
    Vista para ver el detalle de una recepción de artículos.

    Permisos: compras.view_recepcionarticulo
    Utiliza: RecepcionDetailMixin (DRY)
    """
    model = RecepcionArticulo
    template_name = 'compras/recepcion_articulo/detalle.html'
    context_object_name = 'recepcion'
    permission_required = 'compras.view_recepcionarticulo'

    def _optimize_detalles_queryset(self, queryset):
        """Optimiza consultas de detalles con select_related."""
        return queryset.select_related('articulo', 'articulo__categoria')


class RecepcionArticuloCreateView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para crear una nueva recepción de artículos.

    Permisos: compras.add_recepcionarticulo
    Auditoría: Registra acción CREAR automáticamente
    Utiliza: RecepcionArticuloService para lógica de negocio
    """
    model = RecepcionArticulo
    form_class = RecepcionArticuloForm
    template_name = 'compras/recepcion_articulo/form.html'
    permission_required = 'compras.add_recepcionarticulo'

    # Configuración de auditoría
    audit_action = 'CREAR'
    audit_description_template = 'Creó recepción de artículos {obj.numero}'

    # Mensaje de éxito
    success_message = 'Recepción creada exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la recepción creada."""
        return reverse_lazy('compras:recepcion_articulo_detalle', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        from decimal import Decimal
        import json

        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Recepción de Artículos'
        context['action'] = 'Crear'

        # Agregar lista de artículos disponibles
        context['articulos'] = Articulo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria').order_by('codigo')

        # Pasar tipos de recepción en formato JSON
        tipos_recepcion = list(TipoRecepcion.objects.filter(
            activo=True, eliminado=False
        ).values('id', 'codigo', 'nombre', 'requiere_orden'))
        context['tipos_recepcion'] = json.dumps(tipos_recepcion)

        return context

    def form_valid(self, form):
        """Procesa el formulario con generación automática de número y guardado de detalles."""
        from decimal import Decimal
        from core.utils.business import generar_codigo_con_anio
        from django.db import transaction

        try:
            with transaction.atomic():
                # Asignar usuario que recibe
                form.instance.recibido_por = self.request.user

                # Generar número de recepción automáticamente con año
                form.instance.numero = generar_codigo_con_anio('REC-ART', RecepcionArticulo, 'numero', longitud=6)

                # Obtener estado inicial
                estado_repo = EstadoRecepcionRepository()
                estado_inicial = estado_repo.get_inicial()
                if not estado_inicial:
                    form.add_error(None, 'No se encontró un estado inicial para recepciones')
                    return self.form_invalid(form)

                form.instance.estado = estado_inicial

                # Guardar recepción
                response = super().form_valid(form)

                # Procesar detalles de artículos desde el POST
                detalles = self._extraer_detalles_post(self.request.POST)

                if not detalles:
                    form.add_error(None, 'Debe agregar al menos un artículo a la recepción')
                    return self.form_invalid(form)

                # Crear detalles de artículos
                for detalle_data in detalles:
                    DetalleRecepcionArticulo.objects.create(
                        recepcion=self.object,
                        articulo_id=detalle_data['articulo_id'],
                        cantidad=Decimal(str(detalle_data['cantidad'])),
                        lote=detalle_data.get('lote', ''),
                        fecha_vencimiento=detalle_data.get('fecha_vencimiento'),
                        observaciones=detalle_data.get('observaciones', '')
                    )

                messages.success(self.request, self.get_success_message(self.object))
                self.log_action(self.object, self.request)
                return response

        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field if field != '__all__' else None, error)
            return self.form_invalid(form)
        except Exception as e:
            form.add_error(None, f'Error al crear la recepción: {str(e)}')
            return self.form_invalid(form)

    def _extraer_detalles_post(self, post_data):
        """
        Extrae los detalles de artículos del POST.
        Formato esperado: detalles[0][articulo_id], detalles[0][cantidad], etc.
        """
        detalles = []
        indices = set()

        # Identificar todos los índices presentes
        for key in post_data.keys():
            if key.startswith('detalles['):
                # Extraer índice: detalles[0][campo] -> 0
                indice = key.split('[')[1].split(']')[0]
                indices.add(indice)

        # Extraer datos para cada índice
        for indice in indices:
            articulo_id = post_data.get(f'detalles[{indice}][articulo_id]')
            cantidad = post_data.get(f'detalles[{indice}][cantidad]')

            if articulo_id and cantidad:
                detalle = {
                    'articulo_id': int(articulo_id),
                    'cantidad': float(cantidad),
                    'lote': post_data.get(f'detalles[{indice}][lote]', ''),
                    'observaciones': post_data.get(f'detalles[{indice}][observaciones]', '')
                }

                # Fecha de vencimiento (opcional)
                fecha_venc = post_data.get(f'detalles[{indice}][fecha_vencimiento]')
                if fecha_venc:
                    detalle['fecha_vencimiento'] = fecha_venc

                detalles.append(detalle)

        return detalles


class RecepcionArticuloAgregarView(RecepcionAgregarMixin, BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para agregar un artículo a una recepción.

    Permisos: compras.add_detallerecepcionarticulo
    Auditoría: Registra acción CREAR automáticamente
    Utiliza: RecepcionArticuloService y RecepcionAgregarMixin (DRY)
    """
    model = DetalleRecepcionArticulo
    form_class = DetalleRecepcionArticuloForm
    template_name = 'compras/recepcion_articulo/agregar.html'
    permission_required = 'compras.add_detallerecepcionarticulo'

    # Configuración de auditoría
    audit_action = 'CREAR'
    success_message = 'Artículo agregado a la recepción.'

    # Configuración del mixin
    service_class = RecepcionArticuloService
    repository_class = RecepcionArticuloRepository
    item_field_name = 'articulo'
    detail_url_name = 'compras:recepcion_articulo_detalle'

    def get_titulo(self):
        """Título personalizado."""
        return 'Agregar Artículo a Recepción'

    def _preparar_kwargs_detalle(self, form):
        """Prepara argumentos específicos para artículos."""
        return {
            'actualizar_stock': False,  # No actualizar stock hasta confirmar
            'lote': form.cleaned_data.get('lote'),
            'fecha_vencimiento': form.cleaned_data.get('fecha_vencimiento'),
            'observaciones': form.cleaned_data.get('observaciones', '')
        }

    def _get_audit_description(self, recepcion):
        """Descripción de auditoría personalizada."""
        return f'Agregó artículo {self.object.articulo.codigo} a recepción {recepcion.numero}'

    def get_lista_url(self):
        """URL de lista de recepciones."""
        return 'compras:recepcion_articulo_lista'


class RecepcionArticuloConfirmarView(RecepcionConfirmarMixin, BaseAuditedViewMixin, AtomicTransactionMixin, DetailView):
    """
    Vista para confirmar una recepción y actualizar stock.

    Permisos: compras.change_recepcionarticulo
    Auditoría: Registra acción CONFIRMAR automáticamente
    Transacción atómica: Garantiza que stock y movimientos se actualicen correctamente
    Utiliza: RecepcionConfirmarMixin (DRY) con hook para actualizar stock
    """
    model = RecepcionArticulo
    template_name = 'compras/recepcion_articulo/confirmar.html'
    context_object_name = 'recepcion'
    permission_required = 'compras.change_recepcionarticulo'

    # Configuración de auditoría
    audit_action = 'CONFIRMAR'
    audit_description_template = 'Confirmó recepción de artículos {obj.numero}'

    def _post_confirmar_acciones(self, request):
        """Actualiza stock de artículos y crea movimientos."""
        from apps.bodega.repositories import TipoMovimientoRepository
        from apps.bodega.models import Movimiento

        tipo_mov_repo = TipoMovimientoRepository()
        tipo_movimiento = tipo_mov_repo.get_by_codigo('RECEPCION')
        if not tipo_movimiento:
            tipo_movimiento = TipoMovimiento.objects.filter(activo=True).first()

        for detalle in self.object.detalles.filter(eliminado=False):
            articulo = detalle.articulo
            stock_anterior = articulo.stock_actual

            # Actualizar stock
            articulo.stock_actual += detalle.cantidad
            articulo.save()

            # Registrar movimiento
            if tipo_movimiento:
                Movimiento.objects.create(
                    articulo=articulo,
                    tipo=tipo_movimiento,
                    cantidad=detalle.cantidad,
                    operacion='ENTRADA',
                    usuario=request.user,
                    motivo=f'Recepción {self.object.numero}',
                    stock_antes=stock_anterior,
                    stock_despues=articulo.stock_actual
                )

    def get_success_message(self):
        """Mensaje de éxito personalizado."""
        return 'Recepción confirmada y stock actualizado.'

    def get_success_url_after_confirm(self):
        """Redirige al detalle después de confirmar."""
        return f'compras:recepcion_articulo_detalle'


# ==================== VISTAS DE RECEPCIÓN DE ACTIVOS ====================

class RecepcionActivoListView(RecepcionListMixin, BaseAuditedViewMixin, PaginatedListMixin, FilteredListMixin, ListView):
    """
    Vista para listar recepciones de activos.

    Permisos: compras.view_recepcionactivo
    Filtros: Estado
    Utiliza: RecepcionActivoRepository y RecepcionListMixin (DRY)
    """
    model = RecepcionActivo
    template_name = 'compras/recepcion_activo/lista.html'
    context_object_name = 'recepciones'
    permission_required = 'compras.view_recepcionactivo'
    paginate_by = 25
    filter_form_class = RecepcionActivoFiltroForm
    repository_class = RecepcionActivoRepository
    titulo = 'Recepciones de Bienes/Activos'


class RecepcionActivoDetailView(RecepcionDetailMixin, BaseAuditedViewMixin, DetailView):
    """
    Vista para ver el detalle de una recepción de activos.

    Permisos: compras.view_recepcionactivo
    Utiliza: RecepcionDetailMixin (DRY)
    """
    model = RecepcionActivo
    template_name = 'compras/recepcion_activo/detalle.html'
    context_object_name = 'recepcion'
    permission_required = 'compras.view_recepcionactivo'

    def _optimize_detalles_queryset(self, queryset):
        """Optimiza consultas de detalles con select_related."""
        return queryset.select_related('activo')


class RecepcionActivoCreateView(BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para crear una nueva recepción de activos/bienes.

    Permisos: compras.add_recepcionactivo
    Auditoría: Registra acción CREAR automáticamente
    Funcionalidad completa: Generación automática de código, tipos de recepción,
    asociación con OC, y manejo dinámico de detalles (similar a artículos)
    """
    model = RecepcionActivo
    form_class = RecepcionActivoForm
    template_name = 'compras/recepcion_activo/form.html'
    permission_required = 'compras.add_recepcionactivo'

    # Configuración de auditoría
    audit_action = 'CREAR'
    audit_description_template = 'Creó recepción de bienes/activos {obj.numero}'

    # Mensaje de éxito
    success_message = 'Recepción de bienes creada exitosamente.'

    def get_success_url(self) -> str:
        """Redirige al detalle de la recepción creada."""
        return reverse_lazy('compras:recepcion_activo_detalle', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) -> dict:
        """Agrega datos al contexto."""
        from decimal import Decimal
        import json

        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Recepción de Bienes/Activos'
        context['action'] = 'Crear'

        # Agregar lista de activos disponibles
        from apps.activos.models import Activo
        context['activos'] = Activo.objects.filter(
            activo=True, eliminado=False
        ).select_related('categoria').order_by('codigo')

        # Pasar tipos de recepción en formato JSON
        tipos_recepcion = list(TipoRecepcion.objects.filter(
            activo=True, eliminado=False
        ).values('id', 'codigo', 'nombre', 'requiere_orden'))
        context['tipos_recepcion'] = json.dumps(tipos_recepcion)

        # Pasar órdenes de compra disponibles (todas las órdenes activas)
        ordenes_disponibles = OrdenCompra.objects.select_related(
            'proveedor', 'estado'
        ).order_by('-fecha_orden')
        context['ordenes_compra'] = ordenes_disponibles

        return context

    def form_valid(self, form):
        """Procesa el formulario con generación automática de número y guardado de detalles."""
        from decimal import Decimal
        from core.utils.business import generar_codigo_con_anio
        from django.db import transaction

        try:
            with transaction.atomic():
                # Asignar usuario que recibe
                form.instance.recibido_por = self.request.user

                # Generar número de recepción automáticamente con año
                form.instance.numero = generar_codigo_con_anio('REC-ACT', RecepcionActivo, 'numero', longitud=6)

                # Obtener estado inicial
                estado_repo = EstadoRecepcionRepository()
                estado_inicial = estado_repo.get_inicial()
                if not estado_inicial:
                    form.add_error(None, 'No se encontró un estado inicial para recepciones')
                    return self.form_invalid(form)

                form.instance.estado = estado_inicial

                # Guardar recepción
                response = super().form_valid(form)

                # Procesar detalles de activos desde el POST
                detalles = self._extraer_detalles_post(self.request.POST)

                if not detalles:
                    form.add_error(None, 'Debe agregar al menos un bien/activo a la recepción')
                    return self.form_invalid(form)

                # Crear detalles de activos
                for detalle_data in detalles:
                    DetalleRecepcionActivo.objects.create(
                        recepcion=self.object,
                        activo_id=detalle_data['activo_id'],
                        cantidad=Decimal(str(detalle_data['cantidad'])),
                        numero_serie=detalle_data.get('numero_serie', ''),
                        observaciones=detalle_data.get('observaciones', '')
                    )

                messages.success(self.request, self.get_success_message(self.object))
                self.log_action(self.object, self.request)
                return response

        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field if field != '__all__' else None, error)
            return self.form_invalid(form)
        except Exception as e:
            form.add_error(None, f'Error al crear la recepción: {str(e)}')
            return self.form_invalid(form)

    def _extraer_detalles_post(self, post_data):
        """
        Extrae los detalles de activos del POST.
        Formato esperado: detalles[0][activo_id], detalles[0][cantidad], etc.
        """
        detalles = []
        indices = set()

        # Identificar todos los índices presentes
        for key in post_data.keys():
            if key.startswith('detalles['):
                # Extraer índice: detalles[0][campo] -> 0
                indice = key.split('[')[1].split(']')[0]
                indices.add(indice)

        # Extraer datos para cada índice
        for indice in indices:
            activo_id = post_data.get(f'detalles[{indice}][activo_id]')
            cantidad = post_data.get(f'detalles[{indice}][cantidad]')

            if activo_id and cantidad:
                detalle = {
                    'activo_id': int(activo_id),
                    'cantidad': float(cantidad),
                    'numero_serie': post_data.get(f'detalles[{indice}][numero_serie]', ''),
                    'observaciones': post_data.get(f'detalles[{indice}][observaciones]', '')
                }

                detalles.append(detalle)

        return detalles


class RecepcionActivoAgregarView(RecepcionAgregarMixin, BaseAuditedViewMixin, AtomicTransactionMixin, CreateView):
    """
    Vista para agregar un activo a una recepción.

    Permisos: compras.add_detallerecepcionactivo
    Auditoría: Registra acción CREAR automáticamente
    Utiliza: RecepcionActivoService y RecepcionAgregarMixin (DRY)
    """
    model = DetalleRecepcionActivo
    form_class = DetalleRecepcionActivoForm
    template_name = 'compras/recepcion_activo/agregar.html'
    permission_required = 'compras.add_detallerecepcionactivo'

    # Configuración de auditoría
    audit_action = 'CREAR'
    success_message = 'Bien/activo agregado a la recepción.'

    # Configuración del mixin
    service_class = RecepcionActivoService
    repository_class = RecepcionActivoRepository
    item_field_name = 'activo'
    detail_url_name = 'compras:recepcion_activo_detalle'

    def get_titulo(self):
        """Título personalizado."""
        return 'Agregar Bien/Activo a Recepción'

    def _preparar_kwargs_detalle(self, form):
        """Prepara argumentos específicos para activos."""
        return {
            'numero_serie': form.cleaned_data.get('numero_serie'),
            'observaciones': form.cleaned_data.get('observaciones', '')
        }

    def _get_audit_description(self, recepcion):
        """Descripción de auditoría personalizada."""
        return f'Agregó activo {self.object.activo.codigo} a recepción {recepcion.numero}'

    def get_lista_url(self):
        """URL de lista de recepciones."""
        return 'compras:recepcion_activo_lista'


class RecepcionActivoConfirmarView(RecepcionConfirmarMixin, BaseAuditedViewMixin, DetailView):
    """
    Vista para confirmar una recepción de activos.

    Permisos: compras.change_recepcionactivo
    Auditoría: Registra acción CONFIRMAR automáticamente
    Utiliza: RecepcionConfirmarMixin (DRY) sin acciones adicionales
    """
    model = RecepcionActivo
    template_name = 'compras/recepcion_activo/confirmar.html'
    context_object_name = 'recepcion'
    permission_required = 'compras.change_recepcionactivo'

    # Configuración de auditoría
    audit_action = 'CONFIRMAR'
    audit_description_template = 'Confirmó recepción de activos {obj.numero}'

    def get_success_message(self):
        """Mensaje de éxito personalizado."""
        return 'Recepción de bienes confirmada exitosamente.'

    def get_success_url_after_confirm(self):
        """Redirige al detalle después de confirmar."""
        return 'compras:recepcion_activo_detalle'
