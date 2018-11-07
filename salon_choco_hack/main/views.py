from rest_framework import generics
from main import serializers
from main import models

class ServiceList(generics.ListCreateAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceModelSerializer()


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceModelSerializer()


class SalonList(generics.ListCreateAPIView):
    queryset = models.Salon.objects.all()
    serializer_class = serializers.SalonModelSerializer()


class SalonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Salon.objects.all()
    serializer_class = serializers.SalonModelSerializer()