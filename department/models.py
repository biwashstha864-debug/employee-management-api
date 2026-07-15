from django.db import models
from common.models import BaseModel

class Department(BaseModel):
    
    name = models.CharField(
        max_length=20,
        unique=True
    )
    
    code = models.CharField(
        max_length=20,
        unique = True
    )
    
    description = models.TextField(
        blank  = True
    )
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural =  "Departments"
        
    def __str__(self):
        return self.name
    
