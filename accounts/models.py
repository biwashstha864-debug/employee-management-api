from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager

class User(AbstractUser) :
    
    class Role(models.TextChoices):
        ADMIN = "Admin", "ADMIN"
        HR = "HR", "HR"
        MANAGER = "MANAGER","Manager"
        EMPLOYEE = "EMPLOYEE","Employee"
        
        
    email = models.EmailField(unique = True)
     
    role = models.CharField(
         max_length = 20,
         choices = Role.choices,
         default = Role.EMPLOYEE,
     )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
     
    objects  = UserManager()
 
    class Meta :
         verbose_name = "User"
         verbose_name_plural = "Users"

