from django.db import models
from django.conf import settings
from department.models import Department
from common.models import BaseModel

class Designation(BaseModel):
    title = models.CharField(
        max_length=20,
        unique = True,
    )
    
    description = models.TextField(
        blank = True,
    )
    
    class Meta:
        ordering = ["title"]
        verbose_name = "Designation"
        verbose_name_plural = "Designations"
        
    def __str__(self):
        return self.title

class Employee(BaseModel):
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "employee",
    )

    employee_id = models.CharField(
        max_length=20,
        unique  = True,
        editable= False,
    )
    
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name = "employees",
    )
    
    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT,
        related_name = "employees",
    )
    
    salary = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
    )
    
    joining_date = models.DateField()

    phone_number = models.CharField(
        max_length=20,
    )

    address = models.TextField(
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to="employees/profile_pictures/",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["employee_id"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        
       if not self.employee_id:
        last_employee = Employee.objects.order_by("-id").first()

        if last_employee:
            last_id = int(last_employee.employee_id.replace("EMP", ""))
            new_id = last_id + 1
        else:
            new_id = 1

        self.employee_id = f"EMP{new_id:05d}"

        super().save(*args, **kwargs)