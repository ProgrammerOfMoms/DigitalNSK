from rest_framework import serializers

from .models import *

class EventSerializer(serializers.ModelSerializer):
    """Сериализация мероприятия"""
    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "competence",
            "date"
        )

    def create(self,validate_data):
        return Event.objects.create(**validate_data)