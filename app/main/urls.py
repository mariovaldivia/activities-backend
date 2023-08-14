"""App URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from main.views import customers as customer_views
from main.views import contracts as contracts_views
from main.views import activities as activity_views
from main.views import vehicles as vehicle_views

router = DefaultRouter()
router.register(r'customers', customer_views.CustomerViewSet,
                basename='customers')
router.register(r'contracts', contracts_views.ContractViewSet,
                basename='contracts')
router.register(r'activities', activity_views.ActivityViewSet,
                basename='activities')
router.register(r'vehicles', vehicle_views.VehicleViewSet,
                basename='vehicles')
app_name = 'main'
urlpatterns = [
    path('', include(router.urls))
]
