from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    # Rutas específicas primero (antes de la ruta con parámetro)
    path('tipos/', views.lista_reportes, name='lista_reportes'),
    path('historial/', views.historial_reportes, name='historial_reportes'),
    path('inventario-actual/', views.reporte_inventario_actual, name='inventario_actual'),
    path('movimientos/', views.reporte_movimientos, name='movimientos'),
    # Ruta con parámetro de app (debe ir después de las rutas específicas)
    path('<str:app>/', views.dashboard_reportes, name='dashboard_app'),
    # Ruta sin parámetro (dashboard general)
    path('', views.dashboard_reportes, name='dashboard'),
]
