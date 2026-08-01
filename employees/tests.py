from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from department.models import Department
from employees.models import Designation, Employee


class EmployeeAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            email="admin@test.com",
            username="admin",
            password="testpass123",
            role=User.Role.ADMIN,
        )

        self.employee_user = User.objects.create_user(
            email="employee@test.com",
            username="employee",
            password="testpass123",
            role=User.Role.EMPLOYEE,
        )
        self.hr = User.objects.create_user(
            email="hr@test.com",
            username="hr",
            password="testpass123",
            role=User.Role.HR,    
)


        self.department = Department.objects.create(
            name="Information Tech",
            code="IT",
        )

        self.designation = Designation.objects.create(
            title="Software Engineer",
        )

        self.admin_employee = Employee.objects.create(
            user=self.admin,
            department=self.department,
            designation=self.designation,
            salary=50000,
            joining_date=date(2026, 1, 1),
            phone_number="9800000001",
        )

        self.employee = Employee.objects.create(
            user=self.employee_user,
            department=self.department,
            designation=self.designation,
            salary=30000,
            joining_date=date(2026, 2, 1),
            phone_number="9800000002",
        )
        self.hr_employee = Employee.objects.create(
            user=self.hr,
            department=self.department,
            designation=self.designation,
            salary=40000,
            joining_date=date(2026, 3, 1),
            phone_number="9800000003",
)
        
    def test_admin_can_see_all_employees(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        
    def test_employee_can_only_see_themselves(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["employee_id"],
            self.employee.employee_id,
        )
        
    def test_employee_cannot_access_another_employee(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(
            f"/api/employees/{self.admin_employee.id}/"
        )

        self.assertEqual(response.status_code, 404)
        
    def test_negative_salary_is_rejected(self):
        self.client.force_authenticate(user=self.admin)

        new_user = User.objects.create_user(
            email="salary@test.com",
            username="salarytest",
            password="testpass123",
            role=User.Role.EMPLOYEE,
        )

        data = {
            "user": new_user.id,
            "department": self.department.id,
            "designation": self.designation.id,
            "salary": -5000,
            "joining_date": "2026-03-01",
            "phone_number": "9800000003",
        }

        response = self.client.post(
            "/api/employees/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("salary", response.data)
        
    def test_invalid_phone_number_is_rejected(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "user": self.employee_user.id,
            "department": self.department.id,
            "designation": self.designation.id,
            "salary": 30000,
            "joining_date": "2026-03-01",
            "phone_number": "hello",
        }

        response = self.client.post(
            "/api/employees/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone_number", response.data)
    
    
    def test_future_joining_date_is_rejected(self):
        self.client.force_authenticate(user=self.admin)

        new_user = User.objects.create_user(
            email="date@test.com",
            username="datetest",
            password="testpass123",
            role=User.Role.EMPLOYEE,
        )

        data = {
            "user": new_user.id,
            "department": self.department.id,
            "designation": self.designation.id,
            "salary": 30000,
            "joining_date": "2099-01-01",
            "phone_number": "9800000003",
        }

        response = self.client.post(
            "/api/employees/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("joining_date", response.data)
        
    def test_hr_can_see_all_employees(self):
        self.client.force_authenticate(user=self.hr)

        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

        salaries = [
            employee["salary"]
            for employee in response.data["results"]
    ]

        self.assertIn("50000.00", salaries)
        self.assertIn("40000.00", salaries)
        self.assertIn("30000.00", salaries)
    
    def test_employee_can_see_own_salary(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(
        f"/api/employees/{self.employee.id}/"
    )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["salary"], "30000.00")