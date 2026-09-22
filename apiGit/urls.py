from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, UserViewSet, LoanViewSet, StudentViewSet, AuditLogViewSet, SanctionViewSet, ResourceItemViewSet, ResourceTitleViewSet

app_name = 'apiGit'

router = DefaultRouter()
# router.register('example', ExampleViewSet, basename='example')

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'resource-titles', ResourceTitleViewSet, basename='resource-title')
router.register(r'resource-items', ResourceItemViewSet, basename='resource-item')
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'sanctions', SanctionViewSet, basename='sanction')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = router.urls
