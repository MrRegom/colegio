from django.urls import path
from . import views

app_name = 'bodega'

urlpatterns = [
    # Menú principal de bodega
    path('', views.MenuBodegaView.as_view(), name='menu_bodega'),

    # Unidades de Medida (IMPORTANTE: Pertenecen a BODEGA, no a activos)
    path('unidades-medida/', views.UnidadMedidaListView.as_view(), name='lista_unidades'),
    path('unidades-medida/crear/', views.UnidadMedidaCreateView.as_view(), name='unidad_crear'),
    path('unidades-medida/<int:pk>/editar/', views.UnidadMedidaUpdateView.as_view(), name='unidad_editar'),
    path('unidades-medida/<int:pk>/eliminar/', views.UnidadMedidaDeleteView.as_view(), name='unidad_eliminar'),

    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_lista'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria_eliminar'),

    # Artículos
    path('articulos/', views.ArticuloListView.as_view(), name='articulo_lista'),
    path('articulos/crear/', views.ArticuloCreateView.as_view(), name='articulo_crear'),
    path('articulos/<int:pk>/', views.ArticuloDetailView.as_view(), name='articulo_detalle'),
    path('articulos/<int:pk>/editar/', views.ArticuloUpdateView.as_view(), name='articulo_editar'),
    path('articulos/<int:pk>/eliminar/', views.ArticuloDeleteView.as_view(), name='articulo_eliminar'),

    # Movimientos
    path('movimientos/', views.MovimientoListView.as_view(), name='movimiento_lista'),
    path('movimientos/crear/', views.MovimientoCreateView.as_view(), name='movimiento_crear'),
    path('movimientos/<int:pk>/', views.MovimientoDetailView.as_view(), name='movimiento_detalle'),

    # Entregas de Artículos
    path('entregas/articulos/', views.EntregaArticuloListView.as_view(), name='entrega_articulo_lista'),
    path('entregas/articulos/crear/', views.EntregaArticuloCreateView.as_view(), name='entrega_articulo_crear'),
    path('entregas/articulos/<int:pk>/', views.EntregaArticuloDetailView.as_view(), name='entrega_articulo_detalle'),

    # Entregas de Bienes
    path('entregas/bienes/', views.EntregaBienListView.as_view(), name='entrega_bien_lista'),
    path('entregas/bienes/crear/', views.EntregaBienCreateView.as_view(), name='entrega_bien_crear'),
    path('entregas/bienes/<int:pk>/', views.EntregaBienDetailView.as_view(), name='entrega_bien_detalle'),

    # AJAX
    path('ajax/solicitud/<int:solicitud_id>/articulos/', views.obtener_articulos_solicitud, name='ajax_solicitud_articulos'),
]
