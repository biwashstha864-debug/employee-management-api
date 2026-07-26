from rest_framework import viewsets

from .models import Designation,Employee
from .serializers import (
    DesignationSerializer,
    EmployeeWriteSerializer,
    EmployeeReadSerializer
    )


class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = (
        Employee.objects.select_related(
            "user",
            "department",
            "designation",
        )
    )
    def get_serializer_class(self):
        if self.action in ("list","retrieve"):
            return EmployeeReadSerializer
        
        return EmployeeWriteSerializer
