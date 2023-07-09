"""Activities views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from main.permissions.activities import IsOwner

# Filters
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from main.serializers.activities import (
    ActivityModelSerializer, ActivityDetailSerializer,
    WorkerActivitySerializer, VehicleActivitySerializer
)

# Models
from main.models import Activity


class ActivityViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Customer view set."""

    serializer_class = ActivityModelSerializer
    # lookup_field = 'description'

    # Filters
    # filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    # search_fields = ('slug_name', 'name')
    # ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'member_limit')
    # ordering = ('-members__count', '-rides_offered', '-rides_taken')
    # filter_fields = ('verified', 'is_limited')

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Activity.objects.all()
        if self.action == 'list':
            request = self.request
            start = request.GET.get('start')
            end = request.GET.get('end')
            customer = request.GET.get('customer')
            q = queryset.active_activities()
            if start:
                q = q.date(start=start, end=end)
            if customer:
                q = q.filter(customer=customer)
            #     q = q.filter(start__gte=start)
            # if end:
            #     q = q.filter(start__lte=end)
            return q
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActivityDetailSerializer
        return ActivityModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsOwner)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign user who create ."""
        activity = serializer.save()
        activity.created_by = self.request.user
        activity.save()

    @action(detail=True, methods=['post'])
    def add_worker(self, request, pk=None):
        """ Add worker to activity."""
        activity = self.get_object()
        data = request.data
        worker = data['worker']
        if activity.workeractivity_set.filter(worker=worker).exists():
            return Response(
                {'message': 'Worker already registered in activity'},
                status.HTTP_400_BAD_REQUEST)
        serializer = WorkerActivitySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(activity=activity)
        data = {'message': 'Worker added'}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_vehicle(self, request, pk=None):
        """ Add worker to activity."""
        activity = self.get_object()
        data = request.data
        vehicle = data['vehicle']
        if activity.vehicleactivity_set.filter(vehicle=vehicle).exists():
            return Response(
                {'message': 'Vehicle already registered in activity'},
                status.HTTP_400_BAD_REQUEST)
        serializer = VehicleActivitySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(activity=activity)
        data = {'message': 'Vehicle added'}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept_activity(self, request, pk=None):
        """ Change status of activity to accepted."""
        activity = self.get_object()
        activity.status = 'A'
        activity.save()
        data = {'message': 'Activity Accepted'}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def execute_activity(self, request, pk=None):
        """ Change status of activity to accepted."""
        activity = self.get_object()
        activity.status = 'E'
        activity.save()
        data = {'message': 'Activity executed'}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def finish_activity(self, request, pk=None):
        """ Change status of activity to accepted."""
        activity = self.get_object()
        activity.status = 'D'
        activity.save()
        data = {'message': 'Activity done'}
        return Response(data, status=status.HTTP_201_CREATED)
