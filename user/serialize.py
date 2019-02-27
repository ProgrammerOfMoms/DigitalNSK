from rest_framework import serializers

from user.models import *


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""

    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "date_joined",
            "firstName",
            "lastName",
            "photo",
            "patronymic",
            "role"
        )
        extra_kwargs = {'password': {'write_only': True}}

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