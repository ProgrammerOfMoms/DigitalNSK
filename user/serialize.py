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

    def create(self, validate_data):
        user = validate_data.get("id")
        validate_data.pop("id")
        serializer = UserSerializer(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data["id"])
        user = User.objects.get(id = serializer.data["id"])
        return Participant.objects.create(id = user, **validate_data)


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