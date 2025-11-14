import threading

_user = threading.local()

class CurrentUserMiddleware:
    """
    Middleware que guarda temporalmente el usuario en el hilo actual
    para que los signals puedan accederlo.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        _user.value = None  # limpiar después de la petición
        return response


def get_current_user():
    """Obtiene el usuario actual del hilo."""
    return getattr(_user, "value", None)
