from rest_framework import serializers

from user.models import *


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = (
            "id",
            "firstName",
            "lastName",
            "photo",
            "patronymic",
            "role"
        )

class ParticipantSerializer(serializers.ModelSerializer):
    """Сериализация участника"""
    
    id              = UserSerializer()
    #eduInstitution = InstitutionSerializer()
    #passedTests    = TestSerializer(many = True)
    #events         = EventSerializer()

    class Meta:
        model = Participant
        fields = (
            "id",
            "eduInstitution",
            "level",
            "vkURL",
            "instURL",
            "fbURL",
            "passedTests",
            "events",
            "progress"
        )