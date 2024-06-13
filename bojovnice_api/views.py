"""
Views pro API modelu Bojovnice a SkupinyBojovnic.
"""

from rest_framework.viewsets import ReadOnlyModelViewSet
from bojovnice_app import models
from bojovnice_api import serializers

class BojovniceViewSet(ReadOnlyModelViewSet):
    queryset = models.Bojovnice.objects.all()
    serializer_class = serializers.BojovniceSerializer


class SkupinyBojovnicViewSet(ReadOnlyModelViewSet):
    queryset = models.SkupinyBojovnic.objects.all()
    serializer_class = serializers.SkupinyBojovnicSerializer
