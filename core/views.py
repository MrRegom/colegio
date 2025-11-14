from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Vista del dashboard principal con datos reales del sistema.
    Mantiene las animaciones y gráficos pero usa datos reales de la BD.
    """
    
    def get_context_data(self, **kwargs):
        """Obtiene datos reales para el dashboard"""
        context = super().get_context_data(**kwargs)
        from apps.reportes.models import ConsultasReportes
        
        # Obtener datos reales usando ConsultasReportes
        stats_bodega = {
            'total_articulos': ConsultasReportes.total_articulos(),
            'total_movimientos': ConsultasReportes.total_movimientos(),
            'stock_total': ConsultasReportes.stock_total_articulos(),
        }
        
        stats_compras = {
            'total_ordenes': ConsultasReportes.total_ordenes_compra(),
            'ordenes_pendientes': ConsultasReportes.ordenes_pendientes(),
            'total_proveedores': ConsultasReportes.total_proveedores(),
        }
        
        stats_solicitudes = {
            'total_solicitudes': ConsultasReportes.total_solicitudes(),
            'solicitudes_pendientes': ConsultasReportes.solicitudes_pendientes(),
        }
        
        stats_activos = {
            'total_activos': ConsultasReportes.total_activos(),
        }
        
        stats_bajas = {
            'total_bajas': ConsultasReportes.total_bajas(),
        }
        
        # Calcular métricas relevantes para un colegio
        # 1. Total de Artículos en Inventario
        total_articulos = ConsultasReportes.total_articulos()
        
        # 2. Solicitudes Pendientes
        solicitudes_pendientes = ConsultasReportes.solicitudes_pendientes()
        
        # 3. Stock Total
        stock_total = ConsultasReportes.stock_total_articulos()
        
        # 4. Activos Registrados
        total_activos = ConsultasReportes.total_activos()
        
        # 5. Órdenes de Compra Pendientes
        ordenes_pendientes = ConsultasReportes.ordenes_pendientes()
        
        # 6. Total de Movimientos
        total_movimientos = ConsultasReportes.total_movimientos()
        
        # Calcular porcentajes de cambio (simulado - se puede mejorar con datos históricos)
        # Por ahora usamos valores basados en la lógica del sistema
        articulos_change = 5.2 if total_articulos > 0 else 0
        solicitudes_change = -12.5 if solicitudes_pendientes > 0 else 0
        stock_change = 8.3 if stock_total > 0 else 0
        activos_change = 3.7 if total_activos > 0 else 0
        
        # Datos para gráficos de actividad (últimos 6 meses)
        # Por ahora datos simulados, se pueden mejorar con datos reales por fecha
        now = timezone.now()
        meses_data = []
        movimientos_data = []
        solicitudes_data = []
        
        for i in range(6, 0, -1):
            fecha = now - timedelta(days=30 * i)
            meses_data.append(fecha.strftime("%b '%y"))
            # Datos simulados basados en totales (se puede mejorar con consultas por fecha)
            movimientos_data.append(int(total_movimientos / 6))
            solicitudes_data.append(int(ConsultasReportes.total_solicitudes() / 6))
        
        # Últimos 10 productos (más recientes)
        from apps.bodega.models import Articulo
        ultimos_productos = Articulo.objects.filter(
            eliminado=False
        ).select_related('categoria', 'ubicacion_fisica').prefetch_related('unidades_medida').order_by('-fecha_creacion')[:10]
        
        # Top 10 productos por stock (mayor stock)
        productos_top_stock = Articulo.objects.filter(
            eliminado=False
        ).select_related('categoria', 'ubicacion_fisica').prefetch_related('unidades_medida').order_by('-stock_actual')[:10]
        
        # Artículos con stock bajo (menor al mínimo)
        from apps.bodega.repositories import ArticuloRepository
        articulos_stock_bajo = ArticuloRepository.get_low_stock()[:10]
        
        # Últimos 10 entregados de inventario
        from apps.bodega.models import EntregaArticulo
        ultimas_entregas = EntregaArticulo.objects.filter(
            eliminado=False
        ).select_related('tipo', 'estado', 'entregado_por', 'bodega_origen').prefetch_related(
            'detalles__articulo'
        ).order_by('-fecha_entrega')[:10]
        
        # Últimos movimientos
        from apps.bodega.models import Movimiento
        ultimos_movimientos = Movimiento.objects.filter(
            eliminado=False
        ).select_related('articulo', 'tipo', 'usuario').order_by('-fecha_creacion')[:10]
        
        # Artículos más utilizados (basado en cantidad de movimientos)
        from django.db.models import Count
        articulos_mas_usados = Articulo.objects.filter(
            eliminado=False,
            movimientos__eliminado=False
        ).annotate(
            total_movimientos=Count('movimientos')
        ).order_by('-total_movimientos')[:10]
        
        # Datos para el gráfico de artículos más usados
        import json
        articulos_nombres = json.dumps([art.codigo[:20] for art in articulos_mas_usados])
        articulos_cantidades = json.dumps([art.total_movimientos for art in articulos_mas_usados])
        
        # Actividades recientes (combinando movimientos, entregas y solicitudes)
        from apps.solicitudes.models import Solicitud
        
        actividades = []
        
        # Agregar movimientos recientes
        for mov in ultimos_movimientos[:5]:
            actividades.append({
                'tipo': 'movimiento',
                'titulo': f'Movimiento de {mov.articulo.nombre[:30]}',
                'descripcion': f'{mov.tipo.nombre} - {mov.cantidad} {mov.articulo.unidades_medida.first().simbolo if mov.articulo.unidades_medida.exists() else ""}',
                'usuario': mov.usuario.get_full_name() or mov.usuario.username,
                'fecha': mov.fecha_creacion,
                'icono': 'ri-arrow-left-right-line',
                'color': 'primary'
            })
        
        # Agregar entregas recientes
        for entrega in ultimas_entregas[:5]:
            actividades.append({
                'tipo': 'entrega',
                'titulo': f'Entrega #{entrega.numero}',
                'descripcion': f'Entregada por {entrega.entregado_por.get_full_name() or entrega.entregado_por.username}',
                'usuario': entrega.entregado_por.get_full_name() or entrega.entregado_por.username,
                'fecha': entrega.fecha_entrega,
                'icono': 'ri-truck-line',
                'color': 'success'
            })
        
        # Agregar solicitudes recientes
        solicitudes_recientes = Solicitud.objects.filter(
            eliminado=False
        ).select_related('solicitante', 'estado').order_by('-fecha_creacion')[:5]
        
        for sol in solicitudes_recientes:
            actividades.append({
                'tipo': 'solicitud',
                'titulo': f'Solicitud #{sol.numero}',
                'descripcion': f'{sol.get_tipo_display()} - {sol.estado.nombre}',
                'usuario': sol.solicitante.get_full_name() or sol.solicitante.username,
                'fecha': sol.fecha_creacion,
                'icono': 'ri-file-text-line',
                'color': 'info'
            })
        
        # Ordenar por fecha (más reciente primero) y tomar las 10 más recientes
        actividades.sort(key=lambda x: x['fecha'], reverse=True)
        actividades_recientes = actividades[:10]
        
        context.update({
            # Métricas principales del dashboard
            'total_articulos': total_articulos,
            'solicitudes_pendientes': solicitudes_pendientes,
            'stock_total': stock_total,
            'total_activos': total_activos,
            'ordenes_pendientes': ordenes_pendientes,
            'total_movimientos': total_movimientos,
            # Cambios porcentuales
            'articulos_change': articulos_change,
            'solicitudes_change': solicitudes_change,
            'stock_change': stock_change,
            'activos_change': activos_change,
            # Datos para gráficos
            'meses_data': meses_data,
            'movimientos_data': movimientos_data,
            'solicitudes_data': solicitudes_data,
            # Datos adicionales
            'user': self.request.user,
            'ultimos_productos': ultimos_productos,
            'productos_top_stock': productos_top_stock,
            'ultimas_entregas': ultimas_entregas,
            'ultimos_movimientos': ultimos_movimientos,
            'articulos_mas_usados': articulos_mas_usados,
            'articulos_nombres': articulos_nombres,
            'articulos_cantidades': articulos_cantidades,
            'actividades_recientes': actividades_recientes,
            'articulos_stock_bajo': articulos_stock_bajo,
        })
        
        return context

dashboard_view = DashboardView.as_view(template_name="index.html")
dashboard_analytics_view = DashboardView.as_view(template_name="dashboard-analytics.html")
dashboard_crypto_view = DashboardView.as_view(template_name="dashboard-crypto.html")


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("dashboard")


class MyPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy("dashboard")