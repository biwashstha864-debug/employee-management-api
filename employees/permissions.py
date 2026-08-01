from rest_framework.permissions import BasePermission
from accounts.models import User

class IsAdminOrHR(BasePermission):

        def has_permission(self,request,view):
            return request.user.role in  (User.Role.ADMIN,User.Role.HR)
        
