from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    # Menú principal de compras
    path('', views.MenuComprasView.as_view(), name='menu_compras'),

    # ==================== PROVEEDORES ====================
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_lista'),
    path('proveedores/crear/', views.ProveedorCreateView.as_view(), name='proveedor_crear'),
    path('proveedores/<int:pk>/editar/', views.ProveedorUpdateView.as_view(), name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.ProveedorDeleteView.as_view(), name='proveedor_eliminar'),

    # ==================== ÓRDENES DE COMPRA ====================
    path('ordenes/', views.OrdenCompraListView.as_view(), name='orden_compra_lista'),
    path('ordenes/crear/', views.OrdenCompraCreateView.as_view(), name='orden_compra_crear'),
    path('ordenes/<int:pk>/', views.OrdenCompraDetailView.as_view(), name='orden_compra_detalle'),
    path('ordenes/<int:pk>/editar/', views.OrdenCompraUpdateView.as_view(), name='orden_compra_editar'),
    path('ordenes/<int:pk>/agregar-articulo/', views.OrdenCompraAgregarArticuloView.as_view(), name='orden_compra_agregar_articulo'),
    path('ordenes/<int:pk>/agregar-activo/', views.OrdenCompraAgregarActivoView.as_view(), name='orden_compra_agregar_activo'),
    path('ordenes/<int:pk>/eliminar/', views.OrdenCompraDeleteView.as_view(), name='orden_compra_eliminar'),

    # AJAX
    path('api/obtener-detalles-solicitudes/', views.ObtenerDetallesSolicitudesView.as_view(), name='obtener_detalles_solicitudes'),
    path('api/obtener-articulos-orden-compra/', views.ObtenerArticulosOrdenCompraView.as_view(), name='obtener_articulos_orden_compra'),
    path('api/obtener-activos-orden-compra/', views.ObtenerActivosOrdenCompraView.as_view(), name='obtener_activos_orden_compra'),

    # ==================== RECEPCIÓN DE ARTÍCULOS ====================
    path('recepciones-articulos/', views.RecepcionArticuloListView.as_view(), name='recepcion_articulo_lista'),
    path('recepciones-articulos/crear/', views.RecepcionArticuloCreateView.as_view(), name='recepcion_articulo_crear'),
    path('recepciones-articulos/<int:pk>/', views.RecepcionArticuloDetailView.as_view(), name='recepcion_articulo_detalle'),
    path('recepciones-articulos/<int:pk>/agregar/', views.RecepcionArticuloAgregarView.as_view(), name='recepcion_articulo_agregar'),
    path('recepciones-articulos/<int:pk>/confirmar/', views.RecepcionArticuloConfirmarView.as_view(), name='recepcion_articulo_confirmar'),

    # ==================== RECEPCIÓN DE BIENES/ACTIVOS ====================
    path('recepciones-activos/', views.RecepcionActivoListView.as_view(), name='recepcion_activo_lista'),
    path('recepciones-activos/crear/', views.RecepcionActivoCreateView.as_view(), name='recepcion_activo_crear'),
    path('recepciones-activos/<int:pk>/', views.RecepcionActivoDetailView.as_view(), name='recepcion_activo_detalle'),
    path('recepciones-activos/<int:pk>/agregar/', views.RecepcionActivoAgregarView.as_view(), name='recepcion_activo_agregar'),
    path('recepciones-activos/<int:pk>/confirmar/', views.RecepcionActivoConfirmarView.as_view(), name='recepcion_activo_confirmar'),
]
