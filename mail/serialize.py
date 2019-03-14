from rest_framework import serializers

from .models import *
from user.models import User
from user.serialize import UserSerializer


class RecoveryLinkSerializer(serializers.ModelSerializer):
    """Сериализация ссылки на восстановление"""
    
    id        = UserSerializer()


    class Meta:
        model = RecoveryLink
        fields = (
            "id",
            "link",
            # "create_time",
        )
    

    def create(self, validate_data):
        user = validate_data.get("id")
        validate_data.pop("id")
        try:
            user = User.objects.get(id = user["id"])
            serializer = UserSerializer(data = user)
            serializer.is_valid(raise_exception=True)
            return RecoveryLink.objects.create(id = user, **validate_data)

        except User.DoesNotExist as e:
            raise e
            



