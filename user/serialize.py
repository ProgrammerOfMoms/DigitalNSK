from rest_framework import serializers

from institution.serialize import InstitutionSerializer
from testing.serialize import ResultOfTestSerializer
from event.serialize import EventSerializer
from user.models import *

from DigitalNSK import settings

import os

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ProgressSerializer(serializers.ModelSerializer):
    """Сериализация прогресса"""
    event = EventSerializer

    class Meta:
        model = Progress
        fields = (
            "id",
            "progress",
            "event"
        )

    def create(self, validate_data):
        event = validate_data.get("event")
        validate_data.pop("event")
        return Progress.objects.create(event = event, **validate_data)

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
        depth = 5
    
    def create(self, validate_data):
        email = validate_data.get("email")
        password = validate_data.get("password")
        validate_data.pop("email")
        validate_data.pop("password")
        return User.objects.create_user(email = email, password = password, **validate_data)
    
    def update(self, instance, validate_data):
        if "password" in validate_data:
            validate_data.pop("password")
            
        for key in validate_data.keys():
            setattr(instance, key, validate_data[key])

        instance.save()
        return instance

    def update_password(self, instance, old_password, password):
        if instance.check_password(old_password):
                instance.set_password(password) 
        else:
            raise ValueError
        instance.save()
        return instance



class ParticipantSerializer(DynamicFieldsModelSerializer):
    """Сериализация участника"""

    class Meta:
        model = Participant
        fields = (
            "id",
            "eduInstitution",
            "level",
            "vkURL",
            "instURL",
            "fbURL",
        )
        depth = 1

    id              = UserSerializer()
    #eduInstitution  = InstitutionSerializer()
    #passedTests     = ResultOfTestSerializer(many = True)
    #events          = EventSerializer()

    def create(self, validate_data):
        user = validate_data.get("id")
        #progress = validate_data.get("progress")
        #validate_data.pop("progress")
        validate_data.pop("id")
        serializer = UserSerializer(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(id = serializer.data["id"])
        # try:
        #     instituteData = validate_data.get("eduInstitution")
        #     validate_data.pop("eduInstitution")
        #     institute = Institution.objects.get(name = instituteData["name"])
        #     print(institute)
            
        # except Institution.DoesNotExist as e:
        #     raise e
        
        return Participant.objects.create(id = user, **validate_data)
    
   

    def update(self, instance, validate_data):
        for key in validate_data.keys():
            if key == "id":
                try:
                    user = User.objects.get(id = instance.id.id)
                    updateUser = validate_data[key]
                    serializer = UserSerializer(user, updateUser, partial = True)
                    serializer.is_valid(raise_exception = True)
                    serializer.save()
                    setattr(instance, key, user)
                except Exception as e:
                    raise e
            else:
                setattr(instance, key, validate_data[key])
        
        instance.save()
        return instance


    