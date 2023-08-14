"""Customer serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from main.models import Customer


class CustomerModelSerializer(serializers.ModelSerializer):
    """Customer model serializer."""
    identification = serializers.CharField(
        max_length=20,
        validators=[UniqueValidator(queryset=Customer.objects.all())]
    )
    class Meta:
        """Meta class."""

        model = Customer
        fields = (
            'id',
            'name', 'identification',
            'address'
        )
        # read_only_fields = (

        # )
