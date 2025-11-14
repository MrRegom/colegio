# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django-based web application using Python 3.13.2. The system uses a multi-database architecture with SQLite for the main application data and PostgreSQL for read-only employee records.

## Key Commands

### Development Server
```bash
python manage.py runserver
```

### Database Management
```bash
# Run migrations (SQLite only - PostgreSQL is read-only)
python manage.py migrate

# Create migrations for an app
python manage.py makemigrations apps.accounts

# Setup initial data (creates user states, log actions, and superuser)
python manage.py setup_initial_data --usuario admin --correo admin@example.com --contrasena password123
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic
```

### Dependencies
```bash
# Install requirements (note: requeriments.txt has unusual encoding)
pip install -r requeriments.txt
```

## Architecture

### Multi-Database Configuration

The project uses a custom database router (`core/db_router.py`) to manage two databases:

- **default (SQLite)**: Main application database for users, authentication, logs, and application data
- **postgres**: Read-only PostgreSQL database for employee records (funcionarios)

**Important**: PostgreSQL models are read-only. The router prevents migrations and write operations to `postgres_db`. All PostgreSQL models must have `managed = False` in their Meta class.

### Apps Structure

- **apps.accounts**: Authentication, user management, audit logging
  - Custom user state tracking (AuthEstado, AuthUserEstado)
  - Authentication logging (AuthLogs, AuthLogAccion)
  - Login history tracking (HistorialLogin)
  - Custom middleware for thread-local user access (`CurrentUserMiddleware`)

- **apps.pages**: General pages and content management

- **core**: Project configuration, URL routing, and database routing

### Authentication System

Uses **django-allauth** with custom forms:
- Custom login, signup, and password management forms in `apps.accounts.forms`
- Session tracking via `CurrentUserMiddleware` stores authenticated user in thread-local storage
- Login history automatically tracked to `HistorialLogin` model
- Audit logs tracked through `AuthLogs` model

Access thread-local user anywhere in the codebase:
```python
from apps.accounts.middleware import get_current_user
user = get_current_user()
```

### Settings Configuration

Environment variables are managed via **django-environ**. Required `.env` file must include:

```
DJANGO_SECRET_KEY=
DJANGO_DEBUG=
DJANGO_ALLOWED_HOSTS=

# PostgreSQL (read-only)
POSTGRES_ENGINE=
POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

# Email
EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USE_TLS=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
```

### URL Structure

- `/` - Dashboard (requires login)
- `/dashboard_analytics` - Analytics dashboard
- `/dashboard_crypto` - Crypto dashboard
- `/pages/` - General pages
- `/account/` - Authentication (allauth)
- `/admin/` - Django admin panel

### Custom Error Pages

Custom 404 and 500 error handlers are defined in `core/urls.py`:
- `templates/404.html`
- `templates/500.html`

### Static and Media Files

- Static files: `static/` (development) and `staticfiles/` (production)
- Media uploads: `media/`
- Templates: `templates/`

### Template System

Uses Django templates with Bootstrap 5 via crispy-forms:
- Base template: `templates/partials/base.html`
- Topbar partial: `templates/partials/topbar.html`

## Development Notes

### Adding New Apps

1. Create app in `apps/` directory
2. Add to `INSTALLED_APPS` in `core/settings.py`
3. Register URLs in `core/urls.py`
4. Run migrations if needed: `python manage.py makemigrations && python manage.py migrate`

### Working with PostgreSQL Models

PostgreSQL models are **READ-ONLY**:
- Do NOT run migrations for PostgreSQL models
- Set `managed = False` in model Meta
- The database router prevents writes automatically
- Use for display/reporting only, never create/update/delete

### Logging and Auditing

All user actions should be logged via `AuthLogs`:
```python
from apps.accounts.models import AuthLogs, AuthLogAccion

accion = AuthLogAccion.objects.get(glosa='CREAR')
AuthLogs.objects.create(
    usuario=request.user,
    accion=accion,
    descripcion='Descripción de la acción',
    ip_usuario=request.META.get('REMOTE_ADDR'),
    agente=request.META.get('HTTP_USER_AGENT', '')
)
```

### Authentication Flow

Login process:
1. User authenticates via allauth
2. `CurrentUserMiddleware` captures authenticated user in thread-local storage
3. Login tracked in `HistorialLogin` table
4. Audit log created in `AuthLogs` if configured

## Timezone and Localization

- Language: Spanish (`es`)
- Timezone: `America/Santiago`
- All datetime fields use timezone-aware datetimes
