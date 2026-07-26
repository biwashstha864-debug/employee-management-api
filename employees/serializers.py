from rest_framework import serializers
from department.models import Department
from .models import Designation, Employee
from accounts.models import User


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
        )
        
class DepartmentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "code",
        )


class DesignationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = (
            "id",
            "title",
        )
        
class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )
        
class EmployeeReadSerializer(serializers.ModelSerializer):
 department = DepartmentNestedSerializer(read_only=True)
 designation = DesignationNestedSerializer(read_only=True)
 user = UserNestedSerializer(read_only=True)
 class Meta:
        model = Employee
        fields = (
            "id",
            "user",
            "employee_id",
            "department",
            "designation",
            "salary",
            "joining_date",
            "phone_number",
            "address",
            "date_of_birth",
            "created_at",
            "updated_at",
        )
        
class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "user",
            "department",
            "designation",
            "salary",
            "joining_date",
            "phone_number",
            "address",
            "date_of_birth",
        )