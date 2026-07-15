from django.contrib import admin
from .models import Employee,Designation

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at"
    )
    
    search_fields = (
        "title",
    )
    
    ordering = (
        "title",
        )
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "user",
        "department",
        "designation",
        "salary",
        "joining_date"
    )
    
    list_filter = (
        "department",
        "designation",
        "joining_date",
    )
    
    search_fields = (
        "employee_id",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
