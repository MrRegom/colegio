from django.contrib import admin

# Base admin genérico para modelos que heredan de BaseModel
class BaseAdmin(admin.ModelAdmin):
    """
    Admin base que maneja automáticamente created_by y updated_by
    para cualquier modelo que herede de BaseModel.
    """
    # Estos campos no se pueden editar desde el admin
    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si el objeto es nuevo
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
