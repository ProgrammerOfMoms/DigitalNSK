from rest_framework import serializers

from .models import *

class SideCompetenceSerializer(serializers.ModelSerializer):
    """Сериализация компетенции"""
    class Meta:
        model = SideCompetence
        fields = (
            "id",
            "name"
        )

    def create(self,validate_data):
        return SideCompetence.objects.create(**validate_data)

class SideCompetenceAddSerializer(serializers.ModelSerializer):
    """Сериализация компетенции"""
    subCompetence = SideCompetenceSerializer(many = True)

    class Meta:
        model = SideCompetenceAdd
        fields = (
            "id",
            "name",
            "subCompetence"
        )

    def create(self,validate_data):
        competence = validate_data.get("subCompetence")
        competence = SideCompetenceSerializer(competence)
        validate_data.pop("subCompetence")
        return SideCompetenceAdd.objects.create(subCompetence = competence, **validate_data)

class BaseCompetenceSerializer(serializers.ModelSerializer):
    """Сериализация компетенции"""
    subCompetence = SideCompetenceAddSerializer(many = True)

    class Meta:
        model = BaseCompetence
        fields = (
            "id",
            "name",
            "subCompetence"
        )

    def create(self,validate_data):
        competence = validate_data.get("subCompetence")
        competence = SideCompetenceAddSerializer(competence)
        validate_data.pop("subCompetence")
        return BaseCompetence.objects.create(subCompetence = competence, **validate_data)

class MainCompetenceSerializer(serializers.ModelSerializer):
    """Сериализация компетенции"""
    # subCompetence = SideCompetenceAddSerializer(many = True)

    class Meta:
        model = MainCompetence
        fields = (
            "id",
            "name",
        )

    def create(self,validate_data):
        # competence = validate_data.get("subCompetence")
        # competence = SideCompetenceAddSerializer(competence)
        # validate_data.pop("subCompetence")
        return MainCompetence.objects.create(**validate_data)

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
    competence          = SideCompetenceSerializer()
    class Meta:
        model = Point
        fields = (
            "id",
            "value",
            "competence"
        )

    def create(self,validate_data):
        competence = validate_data.get("competence")
        competence = SideCompetenceSerializer(competence)
        validate_data.pop("competence")
        return Event.objects.create(competence = competence, **validate_data)

class EventSerializer(serializers.ModelSerializer):
    """Сериализация мероприятия"""
    #description         = EventStageSerializer(many = True)
    competence          = SideCompetenceSerializer(many = True)
    points              = PointSerializer(many = True)
    mainCompetence      = MainCompetenceSerializer(many = True)

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "img",
            "date",
            "time",
            "description",
            "mainCompetence",
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
        mainCompetences = validate_data.get("mainCompetence")
        competences = validate_data.get("competence")
        points = validate_data.get("points")
        validate_data.pop("mainCompetence")
        validate_data.pop("competence")
        validate_data.pop("points")
        event = Event.objects.create(**validate_data)
        masMainComp = []
        for item in mainCompetences:
            competence = MainCompetence.objects.get(name = item["name"])
            competence.event_m.add(event)
        
        masSideComp = []
        for item in competences:
            competence = SideCompetence.objects.get(name = item["name"])
            competence.event.add(event)

        masPoint = []
        for item in points:
            competence = SideCompetence.objects.get(name = item["competence"]["name"])
            point = Point.objects.create(competence = competence, value = item["value"])
            point.event_add.add(event)
        
        return Event.objects.get(**validate_data)