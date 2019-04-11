from rest_framework import serializers
from News.models import News


class NewsSerializer(serializers.ModelSerializer):
    """Сериализация Новости"""
    class Meta:
        model = News
        fields = (
            'id',
            'html_code',
            'photo',
            'date'
        )


