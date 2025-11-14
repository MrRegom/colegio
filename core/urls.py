"""
URL configuration for judia project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from .views import MyPasswordChangeView, MyPasswordSetView

from core.views import (
    dashboard_view,
    dashboard_analytics_view,
    dashboard_crypto_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # dashboard
    path('', view=dashboard_view, name='dashboard'),
    path('dashboard_analytics', view=dashboard_analytics_view, name='dashboard_analytics'),
    path('dashboard_crypto', view=dashboard_crypto_view, name='dashboard_crypto'),

    # apps
    path('pages/', include('apps.pages.urls')),

    # Apps de inventario
    path('bodega/', include('apps.bodega.urls')),
    path('activos/', include('apps.activos.urls')),
    path('compras/', include('apps.compras.urls')),
    path('solicitudes/', include('apps.solicitudes.urls')),
    path('reportes/', include('apps.reportes.urls')),
    path('bajas-inventario/', include('apps.bajas_inventario.urls')),

    # Gestión de usuarios y permisos
    path('usuarios/', include('apps.accounts.urls')),

    path(
        "account/password/change/",
        login_required(MyPasswordChangeView.as_view()),
        name="account_change_password",
    ),
    path(
        "account/password/set/",
        login_required(MyPasswordSetView.as_view()),
        name="account_set_password",
    ),

    # All Auth 
    path('account/', include('allauth.urls')),
]

def custom_404(request, exception):
    return render(request, "404.html", status=404)

def custom_500(request):
    return render(request, "500.html", status=500)

handler404 = "core.urls.custom_404"
handler500 = "core.urls.custom_500"
