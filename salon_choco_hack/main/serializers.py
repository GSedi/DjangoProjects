from rest_framework.serializers import ModelSerializer
from main.models import (
    Service,
    Salon,
)

class ServiceModelSerializer(ModelSerializer):
    class Meta:
        model = Service,
        fields= '__all__'

class SalonModelSerializer(ModelSerializer):
    class Meta:
        model = Salon,
        fields= '__all__'