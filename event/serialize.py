from rest_framework import serializers

from .models import *

class EventStageSerializer(serializers.ModelSerializer):
    """Сериализация этапа мероприятия"""
    class Meta:
        model = EventStage
        fields = (
            "id",
            "name"
        )

class CompetenceSerializer(serializers.ModelSerializer):
    """Сериализация компетенции"""
    class Meta:
        model = Competence
        fields = (
            "id",
            "name"
        )

class EventSerializer(serializers.ModelSerializer):
    """Сериализация мероприятия"""
    description         = EventStageSerializer(many = True)
    competence          = CompetenceSerializer(many = True)
    inherent_competence = CompetenceSerializer(many = True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "img",
            "date",
            "time",
            "description",
            "competence",
            "inherent_competence",
            "duration",
            "venue",
            "format_event",
            "format_task",
            "max_partiсipants",
            "partiсipants",
            "count",
            "partner",
            "manager_name",
            "manager_position",
            "phonenumber"
        )
        depth = 5

    def create(self,validate_data):
        description = validate_data.get("description")
        competence = validate_data.get("competence")
        inherent_competence = validate_data.get("inherent_competence")
        validate_data.pop("description")
        validate_data.pop("competence")
        validate_data.pop("inherent_competence")
        return Event.objects.create(description = description, competence = competence, inherent_competence = inherent_competence, **validate_data)