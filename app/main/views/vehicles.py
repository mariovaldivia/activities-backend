"""Customer views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
# from rest_framework.permissions import IsAuthenticated
from main.permissions.activities import IsOwner
# Filters
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from main.serializers.vehicles import VehicleModelSerializer

# Models
from main.models import Vehicle


class VehicleViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """ Vehicle view set."""

    serializer_class = VehicleModelSerializer
    lookup_field = 'id'

    search_fields = ('plate')

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Vehicle.objects.all()
        # if self.action == 'list':
        #     return queryset.active_customers()
        return queryset

    def perform_create(self, serializer):
        """Assign created by."""
        customer = serializer.save()
        user = self.request.user
        customer.created_by = user
        customer.save()

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = []
        if self.action in ['update', 'partial_update']:
            permissions.append(IsOwner)
        return [permission() for permission in permissions]
