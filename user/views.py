from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema
from DigitalNSK import settings

import json

from .models import *
from .serialize import UserSerializer, ParticipantSerializer


def getJWT(user):
    payload = jwt_payload_handler(user)
    return jwt.encode(payload, settings.SECRET_KEY)


class SignUp(APIView):
    """
    description: 'This is a sample server Petstore server.'
    """

    permission_classes = (AllowAny,)
    def get(self, request):
        return Response({"doc": self.__doc__})

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            if data["id"]["role"] == User.PARTICIPANT:
                serializer = ParticipantSerializer(data = data, fields = ("id", "level", "token"))
                serializer.is_valid(raise_exception=True)
                serializer.save()

                user = User.objects.get(email = data["id"]["email"])
                token = {"jwt": getJWT(user)}
                
            # elif user["id"]["role"] == User.TUTOR:
            #     serializer = TutorSerializer(data = role)
            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()
            # elif user["id"]["role"] == User.PARTNER:
            #     serializer = PartnerSerializer(data = role)
            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()
            # elif user["id"]["role"] == User.UNIVERSITY:
            #     serializer = UniversitySerializer(data = role)
            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()
            # elif user["id"]["role"] == User.ADMINISTRATOR:
            #     serializer = AdministratorSerializer(data = role)
            #     serializer.is_valid(raise_exception=True)
            #     serializer.save()
            else:
                res = {'error': 'Пользователь не найден'}
                return Response(errors = res, status=status.HTTP_403_FORBIDDEN)
            return Response(data = serializer.data, headers = token, status=status.HTTP_201_CREATED)
        except Exception as e:
            res = {'error': 'Не удалось зарегистрировать пользователя'}
            return Response(errors = res, status=status.HTTP_403_FORBIDDEN)

class SignIn(APIView):
    """Авторизация через email и password"""

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data['email']
            password = data['password']

            user = User.objects.get(email=email, password=password)
            if user:
                try:
                    user_details = {}
                    user_details['email'] = "%s" % (user.email)
                    user_details['firstName'] = "%s" % (user.firstName)
                    user_details['lastName'] = "%s" % (user.lastName)
                    user_details['token'] = getJWT(user)
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    return Response(user_details, status=status.HTTP_201_CREATED)

                except Exception as e:
                    raise e
            else:
                res = {'error': 'Пользователь не найден'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'Пожалуйста, введите email и пароль'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            res = {'error': 'Пользователь не найден'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
