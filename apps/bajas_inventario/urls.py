"""
Configuración de URLs para el módulo de bajas de inventario.

Define todas las rutas para la gestión de bajas de activos y motivos de baja.
"""
from django.urls import path
from . import views

app_name = 'bajas_inventario'

urlpatterns = [
    # ==================== MENÚ PRINCIPAL ====================
    path('', views.MenuBajasView.as_view(), name='menu_bajas'),

    # ==================== BAJAS DE INVENTARIO ====================
    path('listado/', views.BajaInventarioListView.as_view(), name='lista_bajas'),
    path('mis-bajas/', views.MisBajasListView.as_view(), name='mis_bajas'),
    path('crear/', views.BajaInventarioCreateView.as_view(), name='crear_baja'),
    path('<int:pk>/', views.BajaInventarioDetailView.as_view(), name='detalle_baja'),
    path('<int:pk>/editar/', views.BajaInventarioUpdateView.as_view(), name='editar_baja'),
    path('<int:pk>/eliminar/', views.BajaInventarioDeleteView.as_view(), name='eliminar_baja'),

    # ==================== MOTIVOS DE BAJA ====================
    path('motivos/', views.MotivoBajaListView.as_view(), name='lista_motivos'),
    path('motivos/crear/', views.MotivoBajaCreateView.as_view(), name='crear_motivo'),
    path('motivos/<int:pk>/editar/', views.MotivoBajaUpdateView.as_view(), name='editar_motivo'),
    path('motivos/<int:pk>/eliminar/', views.MotivoBajaDeleteView.as_view(), name='eliminar_motivo'),
]
