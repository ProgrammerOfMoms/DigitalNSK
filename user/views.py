from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.renderers import JSONRenderer
from DigitalNSK import settings
from user.actions import *

import json
import copy
import datetime
import uuid

from .models import *
from .serialize import UserSerializer, ParticipantSerializer
from mail.models import RecoveryLink
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

            if "id" in data and data["id"]["role"] == User.PARTICIPANT:
                phone = data["id"]["phoneNumber"]
                serializer = ParticipantSerializer(data = data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                user = User.objects.get(email = data["id"]["email"])
                user.phoneNumber = phone
                user.save()
                data = serializer.data
                res = {"id": data["id"]}
                data.pop("id")
                res.update(data)
                res["jwt"] = getJWT(user)

            elif "role" in data:
                password = uuid.uuid4().hex
                data["password"] = password
                phone = data["phoneNumber"]
                serializer = UserSerializer(data = data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data = serializer.data
                user = User.objects.get(email = data["email"])
                user.phoneNumber = phone
                user.save()
                res = {"jwt": getJWT(user)}
                res.update(data)

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
            if type(res["id"])!=int and "role" in res["id"] and res["id"]["email"] != None:
                data = linkGenerator(id = res["id"]["id"])
                send_confirmation_mail.after_response(email = res["id"]["email"], link = data[0])
            elif "email" in res and res["email"]!=None:
                send_password_for_tutor.after_response(email = res["email"], password = password)
            return Response(data = res, status=status.HTTP_201_CREATED)
        except Exception as e:
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
                    user_details['id'] = "%s" % (user.id)
                    user_details['email'] = "%s" % (user.email)
                    user_details['firstName'] = "%s" % (user.firstName)
                    user_details['lastName'] = "%s" % (user.lastName)
                    user_details['jwt'] = "%s" % (getJWT(user))
                    user_details['role'] = "%s" % (user.role)
                    """
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    """
                    if user.photo!= "":
                        user_details['photo'] = "https://digitalnsk.ru:8000/media/"+user.photo
                    else:
                        user_details['photo'] = "%s"  % (user.photo)
                    if user.role == User.PARTICIPANT:
                        if len(user.participant.passedTests.all())==3:
                            user_details['test'] = True
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

class VKSignIn(APIView):
    """Авторизация через vk"""
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    def post(self, reauest):
        pass


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
                """
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                """
                if res["id"]["photo"] != "":
                    res["id"]["photo"] = "https://digitalnsk.ru:8000/media/"+res["id"]["photo"]
                return Response(data = res, status = status.HTTP_200_OK)
            else:
                serializer = UserSerializer(user)
                data = serializer.data
                return Response(data = data, status = status.HTTP_200_OK)
        
        except User.DoesNotExist:
            res = {"error": "Такого пользователя не существует"}
            return Response(data = res, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise(e)
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            
    
    def put(self, request):
        """Обновление профиля"""
        try:
            id = ""
            try:
                id = request.META["HTTP_ID"]
                user = User.objects.get(id = id)
            except KeyError:
                email = json.loads(request.body.decode("utf-8"))["id"]["email"]
                user = User.objects.get(email = email)
            updateInfo = json.loads(request.body.decode("utf-8"))
            try:
                updateInfo["id"].pop("email")
            except KeyError:
                pass
               

            if user.role == User.PARTICIPANT:
                if "password" in updateInfo["id"]:
                    UserSerializer.update_password(UserSerializer, instance = user, old_password = updateInfo["id"]["password"][0], password = updateInfo["id"]["password"][1])
                    updateInfo["id"].pop("password")
                user = user.participant
                serializer = ParticipantSerializer(user, updateInfo, partial = True)
                serializer.is_valid(raise_exception = True)
                serializer.save()
                data = serializer.data
                res = {"id": data["id"], "eduInstitution": data["eduInstitution"], "level": data["level"]}
                
                
                res["jwt"] = getJWT(user.id)
                return Response(data = res, status = status.HTTP_200_OK)
            else:
                serializer = UserSerializer(user, updateInfo, partial = True)
                serializer.is_valid(raise_exception = True)
                serializer.save()
                data = serializer.data
                data["jwt"] = getJWT(user.id)
                return Response(data = data, status = status.HTTP_200_OK)

        except User.DoesNotExist as e:
            raise(e)
            res = {"error": "Такого пользователя не существует"}
            return Response(data = res, status = status.HTTP_404_NOT_FOUND)
        except ValueError:
            res = {"error": "Пароли не совпадают"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise(e)
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)



class PasswordRecovery(APIView):
    """Отправка и удаление ссылки для восстановления пароля"""

    permission_classes = (AllowAny,)

    def post(self, request):
        # origin = "http://digitalnsk.sibtiger.com/user/recovery-password"
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data["email"]
            id = User.objects.get(email = email).id
            data = linkGenerator(id = id)
            send_password_recovery_link.after_response(email = data[1], link = data[0])
            return Response(status = status.HTTP_200_OK)

        except KeyError as e:
            if e == "HTTP_ID":
                res = {"error":"id не указан"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            else:
                res = {"error": "Неизвестный параметр"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, format=None):
        try:
            hash = json.loads(request.body.decode("utf-8"))["hash"]
            link = RecoveryLink.objects.get(link = hash)
            link.active = False
            return Response(status = status.HTTP_200_OK)

        except RecoveryLink.DoesNotExist:
            res = {"error": "Данной ссылки не найдено"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))["id"]
            link = RecoveryLink.objects.get(link = data["hash"])
            if not link.active:
                res = {"error": "Данной ссылки не найдено"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            user = link.id
            password = {"id":{"password":data["password"]}}
            if user.role == User.PARTICIPANT:
                user = user.participant
                serializer = ParticipantSerializer(user, password, partial = True)
                serializer.is_valid(raise_exception = True)
                serializer.save()
                data = serializer.data
                res = {"id": data["id"]}
                data.pop("id")
                res.update(data)
                res["jwt"] = getJWT(user.id)
                link.delete()
                return Response(data = res, status = status.HTTP_200_OK)

        except RecoveryLink.DoesNotExist:
            res = {"error": "Данной ссылки не найдено"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)


class ConfirmEmail(APIView):
    """Подтверждение электронной почты"""

    permission_classes = (AllowAny,)

    def delete(self, request, format=None):
        try:
            hash = json.loads(request.body.decode("utf-8"))["hash"]
            link = RecoveryLink.objects.get(link = hash)
            user = link.id
            user.emailConfirmed = True
            user.save()
            link.delete()
            return Response(status = status.HTTP_200_OK)

        except RecoveryLink.DoesNotExist:
            res = {"error": "Данной ссылки не найдено"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)


class UploadPhoto(APIView):
    """Загрузка фотографий"""

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            id = request.META["HTTP_ID"]
            photo = request.FILES["photo"]
            link_photo = getPhotoPath(photo = photo, id = id)
            """
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """
            if link_photo:
                return Response(data = {"photo": "https://digitalnsk.ru:8000/media/"+link_photo}, status = status.HTTP_200_OK) 
            else:
                res = {"error": "Пользлвателя с данным id не существует"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            """
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            """
            if user.photo != "":
                res = {"photo": "https://digitalnsk.ru:8000/media/"+user.photo}
            else:
                res = {"photo": None}
            return Response(data = res, status = status.HTTP_200_OK)
        except Exception as e:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)






