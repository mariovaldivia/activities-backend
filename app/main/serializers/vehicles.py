"""Customer serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# Model
from main.models import Vehicle


class VehicleModelSerializer(serializers.ModelSerializer):
    """ Vehicle model serializer."""
    plate = serializers.CharField(
        max_length=10,
        validators=[UniqueValidator(queryset=Vehicle.objects.all())]
    )
    type_name = serializers.CharField(
        source='get_type_name',
        read_only=True
    )

    class Meta:
        """Meta class."""

        model = Vehicle
        fields = (
            'id',
            'brand',
            'model',
            'plate',
            'type',
            'type_name'
        )
