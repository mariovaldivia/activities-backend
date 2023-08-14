"""Customer serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from main.models import Activity, WorkerActivity, VehicleActivity, ActivityLog
from main.serializers.customers import CustomerModelSerializer
from main.serializers.contracts import ContractModelSerializer
from main.serializers.vehicles import VehicleModelSerializer

from users.serializers.users import UserModelSerializer


class ActivityModelSerializer(serializers.ModelSerializer):
    """Activity model serializer."""

    class Meta:
        """Meta class."""

        model = Activity
        fields = (
            'id',
            'description',
            'detail',
            'start',
            'finish',
            'status',
            'created',
            'customer',
            'contract',
            'created_by'
        )
        # read_only_fields = (
        #     'created_by',
        # )

    def validate(self, data):
        """Ensure finish date greater than start """
        start = data.get('start', None)
        finish = data.get('finish', None)
        if start > finish:
            raise serializers.ValidationError(
                'Finish date must be greater than start date')
        return data


class WorkerActivityDetailSerializer(serializers.ModelSerializer):
    """Worker Activity model serializer."""
    worker = UserModelSerializer()

    class Meta:
        """Meta class."""

        model = WorkerActivity
        fields = (
            'worker',
            'role'
        )
        # read_only_fields = (
        #     'created_by',
        # )


class VehicleActivityDetailSerializer(serializers.ModelSerializer):
    """ Vehicle Activity model serializer."""
    vehicle = VehicleModelSerializer()

    class Meta:
        """Meta class."""

        model = VehicleActivity
        fields = (
            'vehicle',
        )
        # read_only_fields = (
        #     'created_by',
        # )


class ActivityLogSerializer(serializers.ModelSerializer):
    """ Activity Log model serializer."""

    class Meta:
        """Meta class."""

        model = ActivityLog
        fields = (
            'status',
            'created'
        )
        read_only_fields = (
            'created_by',
            'created'
        )


class ActivityDetailSerializer(serializers.ModelSerializer):
    """Activity model serializer."""
    customer = CustomerModelSerializer()
    contract = ContractModelSerializer()
    # workers = UserModelSerializer(many=True)
    workers_assigned = WorkerActivityDetailSerializer(
        source='workeractivity_set',
        many=True,
        read_only=True)
    vehicles_assigned = VehicleActivityDetailSerializer(
        source='vehicleactivity_set',
        many=True,
        read_only=True)

    logs = ActivityLogSerializer(
        many=True,
        read_only=True)

    class Meta:
        """Meta class."""

        model = Activity
        fields = (
            'id',
            'status',
            'description',
            'detail',
            'start',
            'finish',
            'created',
            'customer',
            'contract',
            'created_by',
            'workers_assigned',
            'vehicles_assigned',
            'logs'
        )
        # read_only_fields = (
        #     'created_by',
        # )


class WorkerActivitySerializer(serializers.ModelSerializer):
    """Worker Activity model serializer."""

    class Meta:
        """Meta class."""

        model = WorkerActivity
        fields = (
            'worker',
            'role'
        )
        # read_only_fields = (
        #     'created_by',
        # )


class VehicleActivitySerializer(serializers.ModelSerializer):
    """Vehicle Activity model serializer."""

    class Meta:
        """Meta class."""

        model = VehicleActivity
        fields = (
            'vehicle',
            # 'role'
        )
        # read_only_fields = (
        #     'created_by',
        # )
