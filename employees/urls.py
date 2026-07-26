from rest_framework.routers import DefaultRouter

from .views import DesignationViewSet,EmployeeViewSet

router = DefaultRouter()

router.register(
    r"designations",
    DesignationViewSet,
    basename="designation",
)
router.register(
    r"employees",
    EmployeeViewSet,
    basename = "employee"
)
urlpatterns = router.urls