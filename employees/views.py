from rest_framework import viewsets
from accounts.models import User
from .models import Designation,Employee
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    DesignationSerializer,
    EmployeeWriteSerializer,
    EmployeeReadSerializer,
    )
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import EmployeePagination



class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    
class EmployeeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = (
            Employee.objects.select_related(
            "user",
            "department",
            "designation",
        )
    )
   
        if self.request.user.role in (
         User.Role.ADMIN,
         User.Role.HR,
     ):
            return queryset
    
        return queryset.filter(user=self.request.user)


    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EmployeeReadSerializer

        return EmployeeWriteSerializer

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = [
        "employee_id",
        "user__first_name",
        "user__last_name",
        "user__email",
        "phone_number",
    ]
    filterset_fields = [
        "department",
        "designation",
    ]
    ordering_fields = [
    "employee_id",
    "joining_date",
    "created_at",
    "updated_at",
]
    ordering = ["employee_id"]
    
    pagination_class = EmployeePagination
    
