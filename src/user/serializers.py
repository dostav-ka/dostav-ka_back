from rest_framework import serializers

from .models import Courier


class CourierTGSerializer(serializers.Serializer):
    tg_id = serializers.CharField(required=True)
