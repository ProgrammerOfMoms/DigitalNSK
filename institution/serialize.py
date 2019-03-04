from rest_framework import serializers

from user.models import *

class InstitutionSerializer(serializers.ModelSerializer):
    
    """Сериализация учебного заведения"""

    class Meta:
        model = Institution
        fields = (
            "id",
            "name"
        )
