# Sistema de Gestión de Inventario Escolar

Sistema ERP completo para la gestión integral de inventario, compras, solicitudes y activos de un colegio.

## 🎯 Características Principales

- **📦 Gestión de Bodega**: Control completo de artículos, stock, movimientos y entregas
- **💼 Gestión de Activos**: Registro y seguimiento de activos fijos del colegio
- **🛒 Módulo de Compras**: Órdenes de compra, recepciones y gestión de proveedores
- **📋 Solicitudes**: Sistema completo de solicitudes de materiales y activos
- **📊 Reportes**: Reportes y estadísticas del sistema
- **👥 Gestión de Usuarios**: Control de acceso y permisos
- **📉 Bajas de Inventario**: Gestión de bajas y descartes

## 🛠️ Tecnologías

- **Backend**: Django 4.2
- **Base de Datos**: PostgreSQL
- **Frontend**: Bootstrap 5, JavaScript (Vanilla)
- **Arquitectura**: Clean Architecture, Repository Pattern, Service Layer

## 📋 Requisitos Previos

- Python 3.10+
- PostgreSQL 12+
- Node.js (para compilación de assets estáticos)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MrRegom/colegio.git
cd colegio
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DJANGO_SECRET_KEY=tu-secret-key-segura-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_NAME=colegio
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-password-postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-email
DEFAULT_FROM_EMAIL=noreply@colegio.cl
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Cargar datos de ejemplo (opcional)

```bash
python manage.py populate_colegio_data
```

Este comando crea:
- 10 proveedores
- 10 artículos de bodega
- 10 activos
- 10 solicitudes
- Movimientos de inventario

### 8. Crear superusuario

```bash
python manage.py createsuperuser
```

### 9. Recolectar archivos estáticos

```bash
python manage.py collectstatic
```

### 10. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: `http://127.0.0.1:8000`

## 📝 Comandos Útiles

### Poblar datos de ejemplo
```bash
python manage.py populate_colegio_data
```

### Ejecutar tests
```bash
pytest
```

### Crear migraciones
```bash
python manage.py makemigrations
```

### Aplicar migraciones
```bash
python manage.py migrate
```

### Crear superusuario
```bash
python manage.py createsuperuser
```

## 📁 Estructura del Proyecto

```
colegio-app/
├── apps/                    # Aplicaciones Django
│   ├── accounts/           # Gestión de usuarios
│   ├── activos/            # Gestión de activos
│   ├── bodega/             # Gestión de bodega
│   ├── compras/            # Módulo de compras
│   ├── solicitudes/        # Sistema de solicitudes
│   ├── reportes/           # Reportes y estadísticas
│   └── ...
├── core/                   # Configuración principal
│   ├── settings.py        # Configuración Django
│   └── urls.py            # URLs principales
├── templates/              # Plantillas HTML
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos por usuarios
├── fixtures/               # Datos iniciales
└── manage.py              # Script de gestión Django
```

## 🔐 Seguridad

- Las variables sensibles se manejan mediante archivo `.env` (no incluido en el repositorio)
- El archivo `.env` está en `.gitignore` para no subirlo accidentalmente
- Se recomienda usar `DEBUG=False` en producción
- Configurar `ALLOWED_HOSTS` apropiadamente en producción

## 📄 Licencia

Este proyecto es privado y de uso interno.

## 👤 Autor

Desarrollado para gestión de inventario escolar.

## 🤝 Contribuciones

Este es un proyecto privado. Para sugerencias o mejoras, contactar al administrador del sistema.
