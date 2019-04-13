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

    def create(self,validate_data):
        print("competence")
        return Competence.objects.create(**validate_data)

class PointSerializer(serializers.ModelSerializer):
    """Сериализация баллов"""
    competence          = CompetenceSerializer()
    class Meta:
        model = Point
        fields = (
            "id",
            "value",
            "competence"
        )

    def create(self,validate_data):
        competence = validate_data.get("competence")
        competence = CompetenceSerializer(competence)
        validate_data.pop("competence")
        return Event.objects.create(competence = competence, **validate_data)

class EventSerializer(serializers.ModelSerializer):
    """Сериализация мероприятия"""
    #description         = EventStageSerializer(many = True)
    competence          = CompetenceSerializer(many = True)
    points              = PointSerializer(many = True)

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
            "points",
            "venue",
            "format_event",
            "max_partiсipants",
            "partiсipants",
            "partner",
            "manager_name",
            "manager_position",
            "phonenumber"
        )
        depth = 5

    def create(self,validate_data):
        competences = validate_data.get("competence")
        masComp = []
        for competence in competences:
            masComp.append(CompetenceSerializer(competence))
        competence = {"competence": masComp}
        points = validate_data.get("points")
        masPoint = []
        for competence in competences:
            masPoint.append(PointSerializer(points))
        points = {"points": masPoint}
        validate_data.pop("competence")
        validate_data.pop("points")
        return Event.objects.create(competence = competence, points = points, **validate_data)