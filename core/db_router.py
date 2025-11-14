class DatabaseRouter:
    """
    Router para manejar múltiples bases de datos.
    - SQLite para el sistema principal (usuarios, unidades, etc.)
    - PostgreSQL para datos de funcionarios
    """
    
    # Apps que usan PostgreSQL (SOLO LECTURA)
    # Cubrimos tanto el app_label 'apps' (agregado vía proxy) como 'funcionarios'
    # para evitar que consultas caigan por defecto en SQLite.
    postgresql_apps = {'apps', 'funcionarios'}
    
    # Modelos específicos que van a PostgreSQL
    postgresql_models = {
        'funcionario',  # apps.Funcionario (solo lectura)
    }
    
    def db_for_read(self, model, **hints):
        """Sugerir la base de datos para leer."""
        if model._meta.app_label in self.postgresql_apps:
            if model._meta.model_name in self.postgresql_models:
                return 'postgres'
        return 'default'
    
    def db_for_write(self, model, **hints):
        """Sugerir la base de datos para escribir."""
        if model._meta.app_label in self.postgresql_apps:
            if model._meta.model_name in self.postgresql_models:
                return 'postgres'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """Permitir relaciones si los modelos están en la misma base de datos."""
        db_set = {'default', 'postgres'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Controlar qué migraciones van a cada base de datos."""
        if db == 'postgres':
            # PostgreSQL es SOLO LECTURA - no permitir migraciones
            return False
        elif app_label in self.postgresql_apps and model_name in self.postgresql_models:
            # No migrar modelos de PostgreSQL a SQLite
            return False
        return db == 'default'
