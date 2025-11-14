"""
Vistas CRUD para el módulo de inventario.
Proporciona interfaces web completas para gestionar catálogos y entidades de inventario.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView
from .models import (
    Taller, TipoEquipo, Equipo, MantenimientoEquipo,
    Marca, Modelo, NombreArticulo, SectorInventario
)
from .forms import (
    TallerForm, TipoEquipoForm, EquipoForm, MantenimientoEquipoForm,
    BodegaForm, EstadoOrdenCompraForm, EstadoRecepcionForm, ProvenienciaForm, DepartamentoForm,
    MarcaForm, ModeloForm, NombreArticuloForm, SectorInventarioForm
)
from apps.bodega.models import Bodega
from apps.compras.models import EstadoOrdenCompra, EstadoRecepcion
from apps.activos.models import Proveniencia
from apps.solicitudes.models import Departamento


# ==================== TALLERES ====================

@login_required
def taller_list(request):
    """Lista todos los talleres"""
    queryset = Taller.objects.filter(eliminado=False)
    
    # Búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query) |
            Q(ubicacion__icontains=search_query)
        )
    
    # Filtro por activo
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    # Ordenamiento
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    # Paginación
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    }
    return render(request, 'inventario/taller_list.html', context)


@login_required
def taller_create(request):
    """Crear nuevo taller"""
    if request.method == 'POST':
        form = TallerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Taller creado exitosamente.')
            return redirect('inventario:taller_list')
    else:
        form = TallerForm()
    
    return render(request, 'inventario/taller_form.html', {'form': form, 'action': 'Crear'})


@login_required
def taller_update(request, pk):
    """Actualizar taller existente"""
    taller = get_object_or_404(Taller, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = TallerForm(request.POST, instance=taller)
        if form.is_valid():
            form.save()
            messages.success(request, 'Taller actualizado exitosamente.')
            return redirect('inventario:taller_list')
    else:
        form = TallerForm(instance=taller)
    
    return render(request, 'inventario/taller_form.html', {
        'form': form,
        'object': taller,
        'action': 'Editar'
    })


@login_required
def taller_delete(request, pk):
    """Eliminar taller (soft delete)"""
    taller = get_object_or_404(Taller, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        taller.eliminado = True
        taller.activo = False
        taller.save()
        messages.success(request, 'Taller eliminado exitosamente.')
        return redirect('inventario:taller_list')
    
    return render(request, 'inventario/taller_confirm_delete.html', {'object': taller})


# ==================== TIPOS DE EQUIPO ====================

@login_required
def tipo_equipo_list(request):
    """Lista todos los tipos de equipo"""
    queryset = TipoEquipo.objects.filter(eliminado=False)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    }
    return render(request, 'inventario/tipo_equipo_list.html', context)


@login_required
def tipo_equipo_create(request):
    """Crear nuevo tipo de equipo"""
    if request.method == 'POST':
        form = TipoEquipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de equipo creado exitosamente.')
            return redirect('inventario:tipo_equipo_list')
    else:
        form = TipoEquipoForm()
    
    return render(request, 'inventario/tipo_equipo_form.html', {'form': form, 'action': 'Crear'})


@login_required
def tipo_equipo_update(request, pk):
    """Actualizar tipo de equipo existente"""
    tipo = get_object_or_404(TipoEquipo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = TipoEquipoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de equipo actualizado exitosamente.')
            return redirect('inventario:tipo_equipo_list')
    else:
        form = TipoEquipoForm(instance=tipo)
    
    return render(request, 'inventario/tipo_equipo_form.html', {
        'form': form,
        'object': tipo,
        'action': 'Editar'
    })


@login_required
def tipo_equipo_delete(request, pk):
    """Eliminar tipo de equipo (soft delete)"""
    tipo = get_object_or_404(TipoEquipo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        tipo.eliminado = True
        tipo.activo = False
        tipo.save()
        messages.success(request, 'Tipo de equipo eliminado exitosamente.')
        return redirect('inventario:tipo_equipo_list')
    
    return render(request, 'inventario/tipo_equipo_confirm_delete.html', {'object': tipo})


# ==================== EQUIPOS ====================

@login_required
def equipo_list(request):
    """Lista todos los equipos"""
    queryset = Equipo.objects.filter(eliminado=False).select_related('tipo', 'responsable', 'taller')
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query) |
            Q(marca__icontains=search_query) |
            Q(modelo__icontains=search_query) |
            Q(numero_serie__icontains=search_query)
        )
    
    # Filtros
    tipo_filter = request.GET.get('tipo')
    if tipo_filter:
        queryset = queryset.filter(tipo_id=tipo_filter)
    
    estado_filter = request.GET.get('estado')
    if estado_filter:
        queryset = queryset.filter(estado=estado_filter)
    
    taller_filter = request.GET.get('taller')
    if taller_filter:
        queryset = queryset.filter(taller_id=taller_filter)
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para los filtros del formulario
    tipos_equipo = TipoEquipo.objects.filter(activo=True, eliminado=False)
    talleres = Taller.objects.filter(activo=True, eliminado=False)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'tipo_filter': tipo_filter,
        'estado_filter': estado_filter,
        'taller_filter': taller_filter,
        'activo_filter': activo_filter,
        'order_by': order_by,
        'tipos_equipo': tipos_equipo,
        'talleres': talleres,
    }
    return render(request, 'inventario/equipo_list.html', context)


@login_required
def equipo_create(request):
    """Crear nuevo equipo"""
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipo creado exitosamente.')
            return redirect('inventario:equipo_list')
    else:
        form = EquipoForm()
    
    return render(request, 'inventario/equipo_form.html', {'form': form, 'action': 'Crear'})


@login_required
def equipo_update(request, pk):
    """Actualizar equipo existente"""
    equipo = get_object_or_404(Equipo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipo actualizado exitosamente.')
            return redirect('inventario:equipo_list')
    else:
        form = EquipoForm(instance=equipo)
    
    return render(request, 'inventario/equipo_form.html', {
        'form': form,
        'object': equipo,
        'action': 'Editar'
    })


@login_required
def equipo_delete(request, pk):
    """Eliminar equipo (soft delete)"""
    equipo = get_object_or_404(Equipo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        equipo.eliminado = True
        equipo.activo = False
        equipo.save()
        messages.success(request, 'Equipo eliminado exitosamente.')
        return redirect('inventario:equipo_list')
    
    return render(request, 'inventario/equipo_confirm_delete.html', {'object': equipo})


@login_required
def equipo_detail(request, pk):
    """Detalle de equipo con historial de mantenimientos"""
    equipo = get_object_or_404(Equipo, pk=pk, eliminado=False)
    mantenimientos = MantenimientoEquipo.objects.filter(
        equipo=equipo,
        eliminado=False
    ).order_by('-fecha_mantenimiento')
    
    return render(request, 'inventario/equipo_detail.html', {
        'equipo': equipo,
        'mantenimientos': mantenimientos,
    })


# ==================== MANTENIMIENTOS ====================

@login_required
def mantenimiento_create(request, equipo_id):
    """Crear nuevo mantenimiento para un equipo"""
    equipo = get_object_or_404(Equipo, pk=equipo_id, eliminado=False)
    
    if request.method == 'POST':
        form = MantenimientoEquipoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.equipo = equipo
            mantenimiento.save()
            
            # Actualizar fechas del equipo
            equipo.fecha_ultimo_mantenimiento = mantenimiento.fecha_mantenimiento
            if mantenimiento.proximo_mantenimiento:
                equipo.fecha_proximo_mantenimiento = mantenimiento.proximo_mantenimiento
            equipo.save()
            
            messages.success(request, 'Mantenimiento registrado exitosamente.')
            return redirect('inventario:equipo_detail', pk=equipo.id)
    else:
        form = MantenimientoEquipoForm(initial={'equipo': equipo})
    
    return render(request, 'inventario/mantenimiento_form.html', {
        'form': form,
        'equipo': equipo,
        'action': 'Registrar'
    })


# ==================== MENÚ PRINCIPAL DE GESTORES ====================

@login_required
def menu_gestores(request):
    """Menú principal de gestores con estadísticas"""
    from apps.bodega.models import Articulo, Categoria as CategoriaBodega
    from apps.activos.models import CategoriaActivo, UnidadMedida, EstadoActivo
    from apps.compras.models import Proveedor
    
    try:
        stats = {
            'total_bodegas': Bodega.objects.filter(eliminado=False).count(),
            'total_categorias_bodega': CategoriaBodega.objects.filter(eliminado=False).count(),
            'total_categorias_activos': CategoriaActivo.objects.filter(eliminado=False).count(),
            'total_talleres': Taller.objects.filter(eliminado=False).count(),
            'total_equipos': Equipo.objects.filter(eliminado=False).count(),
            'total_proveedores': Proveedor.objects.filter(activo=True).count(),
        }
    except Exception:
        # Si hay error (tablas no existen aún), usar valores por defecto
        stats = {
            'total_bodegas': 0,
            'total_categorias_bodega': 0,
            'total_categorias_activos': 0,
            'total_talleres': 0,
            'total_equipos': 0,
            'total_proveedores': 0,
        }
    
    context = {'stats': stats}
    return render(request, 'inventario/menu_gestores.html', context)


# ==================== BODEGAS ====================

@login_required
def bodega_list(request):
    """Lista todas las bodegas"""
    queryset = Bodega.objects.filter(eliminado=False).select_related('responsable')
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/bodega_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def bodega_create(request):
    """Crear nueva bodega"""
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega creada exitosamente.')
            return redirect('inventario:bodega_list')
    else:
        form = BodegaForm()
    
    return render(request, 'inventario/bodega_form.html', {'form': form, 'action': 'Crear'})


@login_required
def bodega_update(request, pk):
    """Actualizar bodega"""
    bodega = get_object_or_404(Bodega, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = BodegaForm(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega actualizada exitosamente.')
            return redirect('inventario:bodega_list')
    else:
        form = BodegaForm(instance=bodega)
    
    return render(request, 'inventario/bodega_form.html', {
        'form': form,
        'object': bodega,
        'action': 'Editar'
    })


@login_required
def bodega_delete(request, pk):
    """Eliminar bodega (soft delete)"""
    bodega = get_object_or_404(Bodega, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        bodega.eliminado = True
        bodega.activo = False
        bodega.save()
        messages.success(request, 'Bodega eliminada exitosamente.')
        return redirect('inventario:bodega_list')
    
    return render(request, 'inventario/bodega_confirm_delete.html', {'object': bodega})


# ==================== ESTADOS DE ORDEN DE COMPRA ====================

@login_required
def estado_orden_compra_list(request):
    """Lista todos los estados de orden de compra"""
    queryset = EstadoOrdenCompra.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/estado_orden_compra_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def estado_orden_compra_create(request):
    """Crear nuevo estado de orden de compra"""
    if request.method == 'POST':
        form = EstadoOrdenCompraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado creado exitosamente.')
            return redirect('inventario:estado_orden_compra_list')
    else:
        form = EstadoOrdenCompraForm()
    
    return render(request, 'inventario/estado_orden_compra_form.html', {'form': form, 'action': 'Crear'})


@login_required
def estado_orden_compra_update(request, pk):
    """Actualizar estado de orden de compra"""
    estado = get_object_or_404(EstadoOrdenCompra, pk=pk)
    
    if request.method == 'POST':
        form = EstadoOrdenCompraForm(request.POST, instance=estado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado actualizado exitosamente.')
            return redirect('inventario:estado_orden_compra_list')
    else:
        form = EstadoOrdenCompraForm(instance=estado)
    
    return render(request, 'inventario/estado_orden_compra_form.html', {
        'form': form,
        'object': estado,
        'action': 'Editar'
    })


@login_required
def estado_orden_compra_delete(request, pk):
    """Eliminar estado de orden de compra"""
    estado = get_object_or_404(EstadoOrdenCompra, pk=pk)
    
    if request.method == 'POST':
        estado.delete()
        messages.success(request, 'Estado eliminado exitosamente.')
        return redirect('inventario:estado_orden_compra_list')
    
    return render(request, 'inventario/estado_orden_compra_confirm_delete.html', {'object': estado})


# ==================== ESTADOS DE RECEPCIÓN ====================

@login_required
def estado_recepcion_list(request):
    """Lista todos los estados de recepción"""
    queryset = EstadoRecepcion.objects.filter(eliminado=False)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/estado_recepcion_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def estado_recepcion_create(request):
    """Crear nuevo estado de recepción"""
    if request.method == 'POST':
        form = EstadoRecepcionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado creado exitosamente.')
            return redirect('inventario:estado_recepcion_list')
    else:
        form = EstadoRecepcionForm()
    
    return render(request, 'inventario/estado_recepcion_form.html', {'form': form, 'action': 'Crear'})


@login_required
def estado_recepcion_update(request, pk):
    """Actualizar estado de recepción"""
    estado = get_object_or_404(EstadoRecepcion, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = EstadoRecepcionForm(request.POST, instance=estado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado actualizado exitosamente.')
            return redirect('inventario:estado_recepcion_list')
    else:
        form = EstadoRecepcionForm(instance=estado)
    
    return render(request, 'inventario/estado_recepcion_form.html', {
        'form': form,
        'object': estado,
        'action': 'Editar'
    })


@login_required
def estado_recepcion_delete(request, pk):
    """Eliminar estado de recepción (soft delete)"""
    estado = get_object_or_404(EstadoRecepcion, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        estado.eliminado = True
        estado.activo = False
        estado.save()
        messages.success(request, 'Estado eliminado exitosamente.')
        return redirect('inventario:estado_recepcion_list')
    
    return render(request, 'inventario/estado_recepcion_confirm_delete.html', {'object': estado})


# ==================== PROVENIENCIAS ====================

@login_required
def proveniencia_list(request):
    """Lista todas las proveniencias"""
    queryset = Proveniencia.objects.filter(eliminado=False)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/proveniencia_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def proveniencia_create(request):
    """Crear nueva proveniencia"""
    if request.method == 'POST':
        form = ProvenienciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveniencia creada exitosamente.')
            return redirect('inventario:proveniencia_list')
    else:
        form = ProvenienciaForm()
    
    return render(request, 'inventario/proveniencia_form.html', {'form': form, 'action': 'Crear'})


@login_required
def proveniencia_update(request, pk):
    """Actualizar proveniencia"""
    proveniencia = get_object_or_404(Proveniencia, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = ProvenienciaForm(request.POST, instance=proveniencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveniencia actualizada exitosamente.')
            return redirect('inventario:proveniencia_list')
    else:
        form = ProvenienciaForm(instance=proveniencia)
    
    return render(request, 'inventario/proveniencia_form.html', {
        'form': form,
        'object': proveniencia,
        'action': 'Editar'
    })


@login_required
def proveniencia_delete(request, pk):
    """Eliminar proveniencia (soft delete)"""
    proveniencia = get_object_or_404(Proveniencia, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        proveniencia.eliminado = True
        proveniencia.activo = False
        proveniencia.save()
        messages.success(request, 'Proveniencia eliminada exitosamente.')
        return redirect('inventario:proveniencia_list')
    
    return render(request, 'inventario/proveniencia_confirm_delete.html', {'object': proveniencia})


# ==================== DEPARTAMENTOS ====================

@login_required
def departamento_list(request):
    """Lista todos los departamentos"""
    queryset = Departamento.objects.filter(eliminado=False).select_related('responsable')
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/departamento_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def departamento_create(request):
    """Crear nuevo departamento"""
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento creado exitosamente.')
            return redirect('inventario:departamento_list')
    else:
        form = DepartamentoForm()
    
    return render(request, 'inventario/departamento_form.html', {'form': form, 'action': 'Crear'})


@login_required
def departamento_update(request, pk):
    """Actualizar departamento"""
    departamento = get_object_or_404(Departamento, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento actualizado exitosamente.')
            return redirect('inventario:departamento_list')
    else:
        form = DepartamentoForm(instance=departamento)
    
    return render(request, 'inventario/departamento_form.html', {
        'form': form,
        'object': departamento,
        'action': 'Editar'
    })


@login_required
def departamento_delete(request, pk):
    """Eliminar departamento (soft delete)"""
    departamento = get_object_or_404(Departamento, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        departamento.eliminado = True
        departamento.activo = False
        departamento.save()
        messages.success(request, 'Departamento eliminado exitosamente.')
        return redirect('inventario:departamento_list')
    
    return render(request, 'inventario/departamento_confirm_delete.html', {'object': departamento})


# ==================== MARCAS ====================

@login_required
def marca_list(request):
    """Lista todas las marcas"""
    queryset = Marca.objects.filter(eliminado=False)
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'nombre')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/marca_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def marca_create(request):
    """Crear nueva marca"""
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca creada exitosamente.')
            return redirect('inventario:marca_list')
    else:
        form = MarcaForm()
    
    return render(request, 'inventario/marca_form.html', {'form': form, 'action': 'Crear'})


@login_required
def marca_update(request, pk):
    """Actualizar marca"""
    marca = get_object_or_404(Marca, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca actualizada exitosamente.')
            return redirect('inventario:marca_list')
    else:
        form = MarcaForm(instance=marca)
    
    return render(request, 'inventario/marca_form.html', {
        'form': form,
        'object': marca,
        'action': 'Editar'
    })


@login_required
def marca_delete(request, pk):
    """Eliminar marca (soft delete)"""
    marca = get_object_or_404(Marca, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        marca.eliminado = True
        marca.activo = False
        marca.save()
        messages.success(request, 'Marca eliminada exitosamente.')
        return redirect('inventario:marca_list')
    
    return render(request, 'inventario/marca_confirm_delete.html', {'object': marca})


# ==================== MODELOS ====================

@login_required
def modelo_list(request):
    """Lista todos los modelos"""
    queryset = Modelo.objects.filter(eliminado=False).select_related('marca')
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query) |
            Q(marca__nombre__icontains=search_query)
        )
    
    marca_filter = request.GET.get('marca')
    if marca_filter:
        queryset = queryset.filter(marca_id=marca_filter)
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'marca__nombre')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    marcas = Marca.objects.filter(activo=True, eliminado=False)
    
    return render(request, 'inventario/modelo_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'marca_filter': marca_filter,
        'marcas': marcas,
        'order_by': order_by,
    })


@login_required
def modelo_create(request):
    """Crear nuevo modelo"""
    if request.method == 'POST':
        form = ModeloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo creado exitosamente.')
            return redirect('inventario:modelo_list')
    else:
        form = ModeloForm()
    
    return render(request, 'inventario/modelo_form.html', {'form': form, 'action': 'Crear'})


@login_required
def modelo_update(request, pk):
    """Actualizar modelo"""
    modelo = get_object_or_404(Modelo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = ModeloForm(request.POST, instance=modelo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo actualizado exitosamente.')
            return redirect('inventario:modelo_list')
    else:
        form = ModeloForm(instance=modelo)
    
    return render(request, 'inventario/modelo_form.html', {
        'form': form,
        'object': modelo,
        'action': 'Editar'
    })


@login_required
def modelo_delete(request, pk):
    """Eliminar modelo (soft delete)"""
    modelo = get_object_or_404(Modelo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        modelo.eliminado = True
        modelo.activo = False
        modelo.save()
        messages.success(request, 'Modelo eliminado exitosamente.')
        return redirect('inventario:modelo_list')
    
    return render(request, 'inventario/modelo_confirm_delete.html', {'object': modelo})


# ==================== NOMBRES DE ARTÍCULOS ====================

@login_required
def nombre_articulo_list(request):
    """Lista todos los nombres de artículos"""
    queryset = NombreArticulo.objects.filter(eliminado=False).select_related('categoria_recomendada')
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'nombre')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/nombre_articulo_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def nombre_articulo_create(request):
    """Crear nuevo nombre de artículo"""
    if request.method == 'POST':
        form = NombreArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nombre de artículo creado exitosamente.')
            return redirect('inventario:nombre_articulo_list')
    else:
        form = NombreArticuloForm()
    
    return render(request, 'inventario/nombre_articulo_form.html', {'form': form, 'action': 'Crear'})


@login_required
def nombre_articulo_update(request, pk):
    """Actualizar nombre de artículo"""
    nombre_articulo = get_object_or_404(NombreArticulo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = NombreArticuloForm(request.POST, instance=nombre_articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nombre de artículo actualizado exitosamente.')
            return redirect('inventario:nombre_articulo_list')
    else:
        form = NombreArticuloForm(instance=nombre_articulo)
    
    return render(request, 'inventario/nombre_articulo_form.html', {
        'form': form,
        'object': nombre_articulo,
        'action': 'Editar'
    })


@login_required
def nombre_articulo_delete(request, pk):
    """Eliminar nombre de artículo (soft delete)"""
    nombre_articulo = get_object_or_404(NombreArticulo, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        nombre_articulo.eliminado = True
        nombre_articulo.activo = False
        nombre_articulo.save()
        messages.success(request, 'Nombre de artículo eliminado exitosamente.')
        return redirect('inventario:nombre_articulo_list')
    
    return render(request, 'inventario/nombre_articulo_confirm_delete.html', {'object': nombre_articulo})


# ==================== SECTORES DE INVENTARIO ====================

@login_required
def sector_inventario_list(request):
    """Lista todos los sectores de inventario"""
    queryset = SectorInventario.objects.filter(eliminado=False).select_related('responsable')
    
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(codigo__icontains=search_query) |
            Q(nombre__icontains=search_query)
        )
    
    activo_filter = request.GET.get('activo')
    if activo_filter == 'true':
        queryset = queryset.filter(activo=True)
    elif activo_filter == 'false':
        queryset = queryset.filter(activo=False)
    
    order_by = request.GET.get('order_by', 'codigo')
    queryset = queryset.order_by(order_by)
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventario/sector_inventario_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
        'order_by': order_by,
    })


@login_required
def sector_inventario_create(request):
    """Crear nuevo sector de inventario"""
    if request.method == 'POST':
        form = SectorInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sector creado exitosamente.')
            return redirect('inventario:sector_inventario_list')
    else:
        form = SectorInventarioForm()
    
    return render(request, 'inventario/sector_inventario_form.html', {'form': form, 'action': 'Crear'})


@login_required
def sector_inventario_update(request, pk):
    """Actualizar sector de inventario"""
    sector = get_object_or_404(SectorInventario, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        form = SectorInventarioForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sector actualizado exitosamente.')
            return redirect('inventario:sector_inventario_list')
    else:
        form = SectorInventarioForm(instance=sector)
    
    return render(request, 'inventario/sector_inventario_form.html', {
        'form': form,
        'object': sector,
        'action': 'Editar'
    })


@login_required
def sector_inventario_delete(request, pk):
    """Eliminar sector de inventario (soft delete)"""
    sector = get_object_or_404(SectorInventario, pk=pk, eliminado=False)
    
    if request.method == 'POST':
        sector.eliminado = True
        sector.activo = False
        sector.save()
        messages.success(request, 'Sector eliminado exitosamente.')
        return redirect('inventario:sector_inventario_list')
    
    return render(request, 'inventario/sector_inventario_confirm_delete.html', {'object': sector})


# ==================== API AJAX PARA FILTRADO DINÁMICO ====================

from django.http import JsonResponse

@login_required
def ajax_filtrar_modelos(request):
    """Endpoint AJAX para filtrar modelos por marca"""
    marca_id = request.GET.get('marca_id')
    
    if marca_id:
        modelos = Modelo.objects.filter(
            marca_id=marca_id,
            activo=True,
            eliminado=False
        ).values('id', 'codigo', 'nombre')
        return JsonResponse(list(modelos), safe=False)
    
    return JsonResponse([], safe=False)

