from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.models import User, Group, Permission
from django.db import transaction

from .forms import (
    UserCreateForm, UserUpdateForm, UserPasswordChangeForm,
    GroupForm, GroupPermissionsForm, UserGroupsForm, UserPermissionsForm,
    UserFilterForm
)
from .models import AuthLogs, AuthLogAccion

# Importar utilidades centralizadas
from core.utils import registrar_log_auditoria


# ========== MENÚ PRINCIPAL ==========

class MenuUsuariosView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Vista del menú principal de gestión de usuarios"""
    template_name = 'account/gestion_usuarios/menu_usuarios.html'
    permission_required = 'auth.view_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Estadísticas
        context['stats'] = {
            'total_usuarios': User.objects.count(),
            'usuarios_activos': User.objects.filter(is_active=True).count(),
            'usuarios_staff': User.objects.filter(is_staff=True).count(),
            'total_grupos': Group.objects.count(),
        }

        # Permisos del usuario actual
        context['permisos'] = {
            'puede_crear_usuarios': self.request.user.has_perm('auth.add_user'),
            'puede_editar_usuarios': self.request.user.has_perm('auth.change_user'),
            'puede_eliminar_usuarios': self.request.user.has_perm('auth.delete_user'),
            'puede_gestionar_grupos': self.request.user.has_perm('auth.change_group'),
            'puede_gestionar_permisos': self.request.user.has_perm('auth.change_permission'),
        }

        context['titulo'] = 'Gestión de Usuarios y Permisos'

        return context


# ========== GESTIÓN DE USUARIOS ==========

@login_required
@permission_required('auth.view_user', raise_exception=True)
def lista_usuarios(request):
    """Listar todos los usuarios con filtros"""
    form = UserFilterForm(request.GET or None)
    usuarios = User.objects.prefetch_related('groups').all()

    # Aplicar filtros
    if form.is_valid():
        buscar = form.cleaned_data.get('buscar')
        is_active = form.cleaned_data.get('is_active')
        is_staff = form.cleaned_data.get('is_staff')
        group = form.cleaned_data.get('group')

        if buscar:
            usuarios = usuarios.filter(
                Q(username__icontains=buscar) |
                Q(email__icontains=buscar) |
                Q(first_name__icontains=buscar) |
                Q(last_name__icontains=buscar)
            )

        if is_active != '':
            usuarios = usuarios.filter(is_active=is_active)

        if is_staff != '':
            usuarios = usuarios.filter(is_staff=is_staff)

        if group:
            usuarios = usuarios.filter(groups=group)

    # Permisos
    permisos = {
        'puede_crear': request.user.has_perm('auth.add_user'),
        'puede_editar': request.user.has_perm('auth.change_user'),
        'puede_eliminar': request.user.has_perm('auth.delete_user'),
        'puede_cambiar_password': request.user.has_perm('auth.change_user'),
    }

    context = {
        'titulo': 'Listado de Usuarios',
        'usuarios': usuarios,
        'form': form,
        'permisos': permisos,
    }

    return render(request, 'account/gestion_usuarios/lista_usuarios.html', context)


@login_required
@permission_required('auth.view_user', raise_exception=True)
def detalle_usuario(request, pk):
    """Ver detalle de un usuario"""
    usuario = get_object_or_404(User.objects.prefetch_related('groups', 'user_permissions'), pk=pk)

    # Permisos
    permisos = {
        'puede_editar': request.user.has_perm('auth.change_user'),
        'puede_eliminar': request.user.has_perm('auth.delete_user'),
        'puede_cambiar_password': request.user.has_perm('auth.change_user'),
    }

    context = {
        'titulo': f'Usuario: {usuario.username}',
        'usuario_detalle': usuario,
        'permisos': permisos,
    }

    return render(request, 'account/gestion_usuarios/detalle_usuario.html', context)


@login_required
@permission_required('auth.add_user', raise_exception=True)
@transaction.atomic
def crear_usuario(request):
    """Crear un nuevo usuario"""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'CREAR',
                f'Usuario creado: {usuario.username}',
                request
            )

            messages.success(request, f'Usuario {usuario.username} creado exitosamente.')
            return redirect('accounts:detalle_usuario', pk=usuario.pk)
    else:
        form = UserCreateForm()

    context = {
        'titulo': 'Crear Usuario',
        'form': form,
        'action': 'Crear',
    }

    return render(request, 'account/gestion_usuarios/form_usuario.html', context)


@login_required
@permission_required('auth.change_user', raise_exception=True)
@transaction.atomic
def editar_usuario(request, pk):
    """Editar un usuario existente"""
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'ACTUALIZAR',
                f'Usuario actualizado: {usuario.username}',
                request
            )

            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente.')
            return redirect('accounts:detalle_usuario', pk=usuario.pk)
    else:
        form = UserUpdateForm(instance=usuario)

    context = {
        'titulo': f'Editar Usuario: {usuario.username}',
        'form': form,
        'action': 'Actualizar',
        'usuario_detalle': usuario,
    }

    return render(request, 'account/gestion_usuarios/form_usuario.html', context)


@login_required
@permission_required('auth.delete_user', raise_exception=True)
@transaction.atomic
def eliminar_usuario(request, pk):
    """Eliminar (desactivar) un usuario"""
    usuario = get_object_or_404(User, pk=pk)

    # No permitir eliminar superusuarios o el propio usuario
    if usuario.is_superuser:
        messages.error(request, 'No se puede eliminar un superusuario.')
        return redirect('accounts:lista_usuarios')

    if usuario == request.user:
        messages.error(request, 'No puedes eliminarte a ti mismo.')
        return redirect('accounts:lista_usuarios')

    if request.method == 'POST':
        username = usuario.username
        usuario.is_active = False
        usuario.save()

        # Registrar log
        registrar_log_auditoria(
            request.user,
            'ELIMINAR',
            f'Usuario desactivado: {username}',
            request
        )

        messages.success(request, f'Usuario {username} desactivado exitosamente.')
        return redirect('accounts:lista_usuarios')

    context = {
        'titulo': 'Eliminar Usuario',
        'usuario_detalle': usuario,
    }

    return render(request, 'account/gestion_usuarios/eliminar_usuario.html', context)


@login_required
@permission_required('auth.change_user', raise_exception=True)
@transaction.atomic
def cambiar_password_usuario(request, pk):
    """Cambiar contraseña de un usuario"""
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserPasswordChangeForm(request.POST)
        if form.is_valid():
            usuario.set_password(form.cleaned_data['password1'])
            usuario.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'ACTUALIZAR',
                f'Contraseña cambiada para usuario: {usuario.username}',
                request
            )

            messages.success(request, f'Contraseña de {usuario.username} actualizada exitosamente.')
            return redirect('accounts:detalle_usuario', pk=usuario.pk)
    else:
        form = UserPasswordChangeForm()

    context = {
        'titulo': f'Cambiar Contraseña: {usuario.username}',
        'form': form,
        'usuario_detalle': usuario,
    }

    return render(request, 'account/gestion_usuarios/cambiar_password.html', context)


# ========== GESTIÓN DE GRUPOS (ROLES) ==========

@login_required
@permission_required('auth.view_group', raise_exception=True)
def lista_grupos(request):
    """Listar todos los grupos/roles"""
    grupos = Group.objects.annotate(num_usuarios=Count('user')).all()

    # Permisos
    permisos = {
        'puede_crear': request.user.has_perm('auth.add_group'),
        'puede_editar': request.user.has_perm('auth.change_group'),
        'puede_eliminar': request.user.has_perm('auth.delete_group'),
    }

    context = {
        'titulo': 'Listado de Roles/Grupos',
        'grupos': grupos,
        'permisos': permisos,
    }

    return render(request, 'account/gestion_usuarios/lista_grupos.html', context)


@login_required
@permission_required('auth.view_group', raise_exception=True)
def detalle_grupo(request, pk):
    """Ver detalle de un grupo/rol"""
    grupo = get_object_or_404(
        Group.objects.prefetch_related('permissions', 'user_set'),
        pk=pk
    )

    # Permisos
    permisos = {
        'puede_editar': request.user.has_perm('auth.change_group'),
        'puede_eliminar': request.user.has_perm('auth.delete_group'),
    }

    context = {
        'titulo': f'Rol/Grupo: {grupo.name}',
        'grupo': grupo,
        'permisos': permisos,
    }

    return render(request, 'account/gestion_usuarios/detalle_grupo.html', context)


@login_required
@permission_required('auth.add_group', raise_exception=True)
@transaction.atomic
def crear_grupo(request):
    """Crear un nuevo grupo/rol"""
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            grupo = form.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'CREAR',
                f'Grupo/Rol creado: {grupo.name}',
                request
            )

            messages.success(request, f'Rol {grupo.name} creado exitosamente.')
            return redirect('accounts:detalle_grupo', pk=grupo.pk)
    else:
        form = GroupForm()

    context = {
        'titulo': 'Crear Rol/Grupo',
        'form': form,
        'action': 'Crear',
    }

    return render(request, 'account/gestion_usuarios/form_grupo.html', context)


@login_required
@permission_required('auth.change_group', raise_exception=True)
@transaction.atomic
def editar_grupo(request, pk):
    """Editar un grupo/rol existente"""
    grupo = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grupo)
        if form.is_valid():
            grupo = form.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'ACTUALIZAR',
                f'Grupo/Rol actualizado: {grupo.name}',
                request
            )

            messages.success(request, f'Rol {grupo.name} actualizado exitosamente.')
            return redirect('accounts:detalle_grupo', pk=grupo.pk)
    else:
        form = GroupForm(instance=grupo)

    context = {
        'titulo': f'Editar Rol: {grupo.name}',
        'form': form,
        'action': 'Actualizar',
        'grupo': grupo,
    }

    return render(request, 'account/gestion_usuarios/form_grupo.html', context)


@login_required
@permission_required('auth.delete_group', raise_exception=True)
@transaction.atomic
def eliminar_grupo(request, pk):
    """Eliminar un grupo/rol"""
    grupo = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        nombre = grupo.name
        grupo.delete()

        # Registrar log
        registrar_log_auditoria(
            request.user,
            'ELIMINAR',
            f'Grupo/Rol eliminado: {nombre}',
            request
        )

        messages.success(request, f'Rol {nombre} eliminado exitosamente.')
        return redirect('accounts:lista_grupos')

    context = {
        'titulo': 'Eliminar Rol/Grupo',
        'grupo': grupo,
    }

    return render(request, 'account/gestion_usuarios/eliminar_grupo.html', context)


# ========== ASIGNACIÓN DE PERMISOS Y GRUPOS ==========

@login_required
@permission_required('auth.change_group', raise_exception=True)
@transaction.atomic
def asignar_permisos_grupo(request, pk):
    """Asignar permisos a un grupo"""
    grupo = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        form = GroupPermissionsForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'ACTUALIZAR',
                f'Permisos actualizados para grupo: {grupo.name}',
                request
            )

            messages.success(request, f'Permisos del rol {grupo.name} actualizados exitosamente.')
            return redirect('accounts:detalle_grupo', pk=grupo.pk)
    else:
        form = GroupPermissionsForm(instance=grupo)

    # Organizar permisos por app
    permisos_organizados = {}
    for permission in form.fields['permissions'].queryset:
        app_label = permission.content_type.app_label
        if app_label not in permisos_organizados:
            permisos_organizados[app_label] = []
        permisos_organizados[app_label].append(permission)

    context = {
        'titulo': f'Asignar Permisos: {grupo.name}',
        'form': form,
        'grupo': grupo,
        'permisos_organizados': permisos_organizados,
    }

    return render(request, 'account/gestion_usuarios/asignar_permisos_grupo.html', context)


@login_required
@permission_required('auth.change_user', raise_exception=True)
@transaction.atomic
def asignar_grupos_usuario(request, pk):
    """Asignar grupos/roles a un usuario"""
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserGroupsForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'ACTUALIZAR',
                f'Grupos actualizados para usuario: {usuario.username}',
                request
            )

            messages.success(request, f'Roles del usuario {usuario.username} actualizados exitosamente.')
            return redirect('accounts:detalle_usuario', pk=usuario.pk)
    else:
        form = UserGroupsForm(instance=usuario)

    context = {
        'titulo': f'Asignar Roles: {usuario.username}',
        'form': form,
        'usuario_detalle': usuario,
    }

    return render(request, 'account/gestion_usuarios/asignar_grupos_usuario.html', context)


@login_required
@permission_required('auth.change_user', raise_exception=True)
@transaction.atomic
def asignar_permisos_usuario(request, pk):
    """Asignar permisos específicos a un usuario"""
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserPermissionsForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()

            # Registrar log
            registrar_log_auditoria(
                request.user,
                'ACTUALIZAR',
                f'Permisos actualizados para usuario: {usuario.username}',
                request
            )

            messages.success(request, f'Permisos del usuario {usuario.username} actualizados exitosamente.')
            return redirect('accounts:detalle_usuario', pk=usuario.pk)
    else:
        form = UserPermissionsForm(instance=usuario)

    # Organizar permisos por app
    permisos_organizados = {}
    for permission in form.fields['user_permissions'].queryset:
        app_label = permission.content_type.app_label
        if app_label not in permisos_organizados:
            permisos_organizados[app_label] = []
        permisos_organizados[app_label].append(permission)

    context = {
        'titulo': f'Asignar Permisos: {usuario.username}',
        'form': form,
        'usuario_detalle': usuario,
        'permisos_organizados': permisos_organizados,
    }

    return render(request, 'account/gestion_usuarios/asignar_permisos_usuario.html', context)
