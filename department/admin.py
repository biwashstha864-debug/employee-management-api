from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "description",
        "created_at",
        "updated_at"
    )
    
    search_fields = (
        "name",
        "code"
    )
    
    ordering_by = ("name",)
    
