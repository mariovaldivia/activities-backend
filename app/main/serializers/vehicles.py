"""Customer serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from main.models import Vehicle


class VehicleModelSerializer(serializers.ModelSerializer):
    """ Vehicle model serializer."""

    class Meta:
        """Meta class."""

        model = Vehicle
        fields = (
            'id',
            'brand',
            'model',
            'plate',
            'type'
        )

    # def validate(self, data):
    #     """Ensure both members_limit and is_limited are present."""
    #     members_limit = data.get('members_limit', None)
    #     is_limited = data.get('is_limited', False)
    #     if is_limited ^ bool(members_limit):
    #         raise serializers.ValidationError('If circle is limited, a member limit must be provided')
    #     return data
