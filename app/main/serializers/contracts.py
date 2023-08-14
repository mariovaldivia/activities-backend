"""Customer serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# Model
from main.models import Contract


class ContractModelSerializer(serializers.ModelSerializer):
    """Contract model serializer."""
    customer_name = serializers.CharField(
        source='get_customer_name',
        read_only=True
    )
    identification = serializers.CharField(
        max_length=20,
        validators=[UniqueValidator(queryset=Contract.objects.all())]
    )

    class Meta:
        """Meta class."""

        model = Contract
        fields = (
            'id',
            'customer_name',
            'description', 'identification',
            'customer',
            'detail',
            'start',
            'finish'
        )


    def validate(self, data):
        """Ensure finish date greater than start """
        start = data.get('start', None)
        finish = data.get('finish', None)
        if start > finish:
            raise serializers.ValidationError(
                'Finish date must be greater than start date')
        return data
