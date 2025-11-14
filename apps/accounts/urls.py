from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Menú principal
    path('', views.MenuUsuariosView.as_view(), name='menu_usuarios'),

    # Gestión de Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:pk>/cambiar-password/', views.cambiar_password_usuario, name='cambiar_password_usuario'),

    # Asignación de roles y permisos a usuarios
    path('usuarios/<int:pk>/asignar-grupos/', views.asignar_grupos_usuario, name='asignar_grupos_usuario'),
    path('usuarios/<int:pk>/asignar-permisos/', views.asignar_permisos_usuario, name='asignar_permisos_usuario'),

    # Gestión de Grupos/Roles
    path('grupos/', views.lista_grupos, name='lista_grupos'),
    path('grupos/<int:pk>/', views.detalle_grupo, name='detalle_grupo'),
    path('grupos/crear/', views.crear_grupo, name='crear_grupo'),
    path('grupos/<int:pk>/editar/', views.editar_grupo, name='editar_grupo'),
    path('grupos/<int:pk>/eliminar/', views.eliminar_grupo, name='eliminar_grupo'),

    # Asignación de permisos a grupos
    path('grupos/<int:pk>/asignar-permisos/', views.asignar_permisos_grupo, name='asignar_permisos_grupo'),
]
