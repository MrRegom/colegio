from crispy_forms.helper import FormHelper
from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm, SetPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import AuthEstado


class UserLoginForm(LoginForm):
    """Formulario de login personalizado con estilos Bootstrap."""
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['login'].widget = forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su usuario',
            'id': 'username'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2 position-relative',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password'
        })
        self.fields['remember'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })


class UserRegistrationForm(SignupForm):
    """Formulario de registro personalizado con estilos Bootstrap."""
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su email',
            'id': 'email'
        })
        self.fields['email'].label = "Email"
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su usuario',
            'id': 'username1'
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password1'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su contraseña nuevamente',
            'id': 'password2'
        })
        self.fields['password2'].label = "Confirmar contraseña"


class PasswordChangeForm(ChangePasswordForm):
    """Formulario de cambio de contraseña personalizado."""
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['oldpassword'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su contraseña actual',
            'id': 'password3'
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su nueva contraseña',
            'id': 'password4'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su nueva contraseña nuevamente',
            'id': 'password5'
        })
        self.fields['oldpassword'].label = "Contraseña actual"
        self.fields['password2'].label = "Confirmar contraseña"


class PasswordResetForm(ResetPasswordForm):
    """Formulario de reseteo de contraseña personalizado."""
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su email',
            'id': 'email1'
        })
        self.fields['email'].label = "Email"


class PasswordResetKeyForm(ResetPasswordKeyForm):
    """Formulario de reseteo de contraseña con clave personalizado."""
    def __init__(self, *args, **kwargs):
        super(PasswordResetKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su nueva contraseña',
            'id': 'password6'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su nueva contraseña nuevamente',
            'id': 'password7'
        })
        self.fields['password2'].label = "Confirmar contraseña"


class PasswordSetForm(SetPasswordForm):
    """Formulario de establecimiento de contraseña personalizado."""
    def __init__(self, *args, **kwargs):
        super(PasswordSetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control mb-2',
            'placeholder': 'Ingrese su nueva contraseña',
            'id': 'password8'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña nuevamente',
            'id': 'password9'
        })
        self.fields['password2'].label = "Confirmar contraseña"


# ========== FORMULARIOS DE GESTIÓN DE USUARIOS ==========

class UserCreateForm(forms.ModelForm):
    """Formulario para crear nuevos usuarios del sistema."""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme la contraseña'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': 'Usuario Activo',
            'is_staff': 'Es Staff',
            'is_superuser': 'Es Superusuario',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar usuarios del sistema."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': 'Usuario Activo',
            'is_staff': 'Es Staff',
            'is_superuser': 'Es Superusuario',
        }


class UserPasswordChangeForm(forms.Form):
    """Formulario para cambiar contraseña de usuario (por admin)."""
    password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme la contraseña'
        })
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2


# ========== FORMULARIOS DE GESTIÓN DE GRUPOS/ROLES ==========

from django.contrib.auth.models import Group, Permission

class GroupForm(forms.ModelForm):
    """Formulario para crear/editar grupos (roles)."""
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del rol'
            }),
        }
        labels = {
            'name': 'Nombre del Rol',
        }


class GroupPermissionsForm(forms.ModelForm):
    """Formulario para asignar permisos a un grupo."""
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permisos'
    )

    class Meta:
        model = Group
        fields = ['permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Organizar permisos por app/modelo
        self.fields['permissions'].queryset = Permission.objects.select_related(
            'content_type'
        ).order_by('content_type__app_label', 'content_type__model', 'codename')


class UserGroupsForm(forms.ModelForm):
    """Formulario para asignar grupos a un usuario."""
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Roles/Grupos'
    )

    class Meta:
        model = User
        fields = ['groups']


class UserPermissionsForm(forms.ModelForm):
    """Formulario para asignar permisos específicos a un usuario."""
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permisos del Usuario'
    )

    class Meta:
        model = User
        fields = ['user_permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Organizar permisos por app/modelo
        self.fields['user_permissions'].queryset = Permission.objects.select_related(
            'content_type'
        ).order_by('content_type__app_label', 'content_type__model', 'codename')


# ========== FORMULARIOS DE FILTROS ==========

class UserFilterForm(forms.Form):
    """Formulario para filtrar usuarios."""
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, email, usuario...'
        }),
        label='Buscar'
    )
    is_active = forms.TypedChoiceField(
        required=False,
        coerce=lambda x: x == 'True',
        choices=[
            ('', 'Todos los estados'),
            ('True', 'Activos'),
            ('False', 'Inactivos')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Estado'
    )
    is_staff = forms.TypedChoiceField(
        required=False,
        coerce=lambda x: x == 'True',
        choices=[
            ('', 'Todos'),
            ('True', 'Staff'),
            ('False', 'No Staff')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Es Staff'
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        empty_label='Todos los roles',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Rol/Grupo'
    )



