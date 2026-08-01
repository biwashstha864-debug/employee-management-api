from rest_framework import serializers
from department.models import Department
from .models import Designation, Employee
from accounts.models import User
from django.utils import timezone


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
            "phone_number",
            "address",
            "date_of_birth",
            "salary",
            "joining_date",
        )
        
    def validate_salary(self,value):
            if value<0 :
                raise serializers.ValidationError(
                    "salary cannot be negative"
                )
            return value
    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
            "Phone number must contain only digits."
        )

        if len(value) != 10:
            raise serializers.ValidationError(
            "Phone number must be exactly 10 digits."
        )

        return value
        
    def validate_joining_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError(
            "Joining date cannot be in the future."
        )

        return value