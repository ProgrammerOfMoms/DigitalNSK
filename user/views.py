from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.schemas import ManualSchema
from rest_framework.renderers import JSONRenderer
import coreapi
import coreschema
from DigitalNSK import settings

import json
import copy

from .models import *
from .serialize import UserSerializer, ParticipantSerializer
from mail.linkGenerator import linkGenerator
from mail.actions import *


def getJWT(user):
    payload = jwt_payload_handler(user)
    return jwt.encode(payload, settings.SECRET_KEY)


class SignUp(APIView):
    """Регистрация через email и password"""

    permission_classes = (AllowAny,)
    def get(self, request):
        return Response({"doc": self.__doc__})

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))

            if data["id"]["role"] == User.PARTICIPANT:
                serializer = ParticipantSerializer(data = data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                user = User.objects.get(email = data["id"]["email"])
                data = serializer.data
                res = {"id": data["id"]}
                data.pop("id")
                res.update(data)
                res["jwt"] = getJWT(user)

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
                return Response(data = res, status=status.HTTP_403_FORBIDDEN)
            

            return Response(data = res, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e
            res = {'error': 'Не удалось зарегистрировать пользователя'}
            return Response(data = res, status=status.HTTP_403_FORBIDDEN)
                



class SignIn(APIView):
    """Авторизация через email и password"""

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data['email']
            password = data['password']

            user = authenticate(email = email, password = password)
            if user:
                try:
                    user_details = {}
                    user_details['email'] = "%s" % (user.email)
                    user_details['firstName'] = "%s" % (user.firstName)
                    user_details['lastName'] = "%s" % (user.lastName)
                    user_details['jwt'] = "%s" % (getJWT(user))
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    return Response(data = user_details, status=status.HTTP_201_CREATED)
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


class Profile(APIView):
    """Редактирование профиля"""

    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request):
        """Получение информации о пользователе"""
        
        try:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)

            if user.role == User.PARTICIPANT:
                user = user.participant
                serializer = ParticipantSerializer(user)
                data = serializer.data
                res = {"id": data["id"]}
                data.pop("id")
                res.update(data)
                return Response(data = res, status = status.HTTP_200_OK)
        
        except User.DoesNotExist:
            res = {"error": "Такого пользователя не существует"}
            return Response(data = res, status = status.HTTP_404_NOT_FOUND)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            
    
    def put(self, request):
        """Обновление профиля"""

        try:
            id = request.META["HTTP_ID"]
            updateParticipant = json.loads(request.body.decode("utf-8"))
            user = User.objects.get(id = id)   

            if user.role == User.PARTICIPANT:
                user = user.participant
                serializer = ParticipantSerializer(user, updateParticipant, partial = True)
                serializer.is_valid(raise_exception = True)
                serializer.save()
                data = serializer.data
                res = {"id": data["id"]}
                data.pop("id")
                res.update(data)
                return Response(data = res, status = status.HTTP_200_OK)
            
            """Здесь остальные роли"""

        except User.DoesNotExist:
            res = {"error": "Такого пользователя не существует"}
            return Response(data = res, status = status.HTTP_404_NOT_FOUND)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)


class PasswordRecovery(APIView):
    """Отправка ссылки для восстановления пароля"""

    permission_classes = (AllowAny,)

    def post(self, request):
        # origin = "http://digitalnsk.sibtiger.com/user/recovery-password"
        try:
            email = json.loads(request.body.decode("utf-8"))["email"]
            id = User.objects.get(email = email).id
            data = linkGenerator(id = id)
            print(data)
            send_password_recovery_link.after_response(email = data[1], link = data[0])
            return Response(status = status.HTTP_200_OK)

        except KeyError as e:
            if e == "HTTP_ID":
                res = {"error":"id не указан"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            else:
                res = {"error": "Неизвестный параметр "+e}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

# class PasswordRecoveryAccept(APIView):
#     def get



