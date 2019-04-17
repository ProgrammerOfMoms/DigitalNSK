from rest_framework import serializers
from news.models import News
from DigitalNSK import settings

import os
import uuid
import random
import copy

#settings.MEDIA_ROOT
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
    
    def create(self, validate_data):
        return News.objects.create(**validate_data)



