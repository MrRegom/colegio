from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password


class UserBaseManager(UserManager):
    """
    Manager personalizado para usuarios con campos en español.
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Crear usuario con campos en español."""
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        
        # Mapear campos en español a campos estándar de Django
        extra_fields.setdefault('first_name', extra_fields.pop('nombres', ''))
        extra_fields.setdefault('last_name', extra_fields.pop('apellidos', ''))
        extra_fields.setdefault('is_staff', extra_fields.pop('staff', False))
        extra_fields.setdefault('is_superuser', extra_fields.pop('superusuario', False))
        
        # Crear usuario estándar
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Crear superusuario con campos en español."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(username, email, password, **extra_fields)
