from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from DigitalNSK import settings
from user.actions import *

import json
import copy
import datetime
import requests
import uuid
import openpyxl
import threading
import after_response

from .models import *
from .serialize import UserSerializer, ParticipantSerializer
from mail.models import RecoveryLink
from mail.linkGenerator import linkGenerator
from mail.actions import *

import vk_api

def getJWT(user):
    payload = jwt_payload_handler(user)
    return jwt.encode(payload, settings.SECRET_KEY)

class TestClass(APIView):
    """Тест токена"""
    permission_classes = (IsAuthenticated,)

    def get(self, requset):
        serializer = UserSerializer(requset.user)
        return Response(serializer.data, status = status.HTTP_200_OK)

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


# https://oauth.vk.com/authorize?client_id=6980768&display=page&redirect_uri=https://digitalnsk.ru/&scope=email&photots&response_type=code&v=5.95
class VKSignIn(APIView):
    """Авторизация через vk"""
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request):
        try:
            root_url = "https://oauth.vk.com/access_token?"
            if "code" in request.data:
                code = request.data["code"]
            res = requests.get(root_url+"client_id="+settings.APP_ID_VK+"&client_secret="+settings.PRIVATE_KEY_VK+"&redirect_uri="+settings.REDIRECT_URI+"&code="+code)
            content = res.json()
            if "error" in content:
                error = content
                raise ValueError
            vk = auth(content["access_token"])
            id = content["user_id"]

            if len(User.objects.filter(email = str(id))) == 0:
                user = vk.method("users.get", {"user_ids": [id], "fields": ["photo_50"]})[0]
                data = {
                    "id": {
                        "email": str(id),
                        "firstName": user["first_name"],
                        "lastName": user["last_name"],
                        "role": User.PARTICIPANT,
                        "password": uuid.uuid4().hex,
                        "photo": user["photo_50"]
                    }
                }
                serializer = ParticipantSerializer(data = data)
                serializer.is_valid(raise_exception=False)
                serializer.save()
                user = User.objects.get(email = str(id))
                user.is_social = True
                user.save()
            else:
                user = User.objects.get(email = str(id))
            res = {}
            res['id'] = "%s" % (user.id)
            res['email'] = "%s" % (user.email)
            res['firstName'] = "%s" % (user.firstName)
            res['lastName'] = "%s" % (user.lastName)
            res['role'] = "%s" % (user.role)
            res['photo'] = "%s" % (user.photo)
            res["jwt"] = getJWT(user)
            res["social"] = "vk"
            if len(user.participant.passedTests.all())==3:
                res['test'] = True
            return Response(data = res, status=status.HTTP_201_CREATED)
        except ValueError:
            res = error
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        except:
            res = {'error': 'Неизвестная ошибка'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

# https://graph.facebook.com/v3.3/oauth/access_token?
#    client_id={app-id}
#    &redirect_uri={redirect-uri}
#    &client_secret={app-secret}
#    &code={code-parameter}
#  "https://graph.facebook.com/{your-user-id}
#    ?fields=id,name
#    &access_token={your-user-access-token}"
class FaceBookSignIn(APIView):
    "Авторизация через facebook"

    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request):
        try:
            root_url = "https://graph.facebook.com/v3.3/oauth/access_token?"
            if "code" in request.data:
                code = request.data["code"]
            res = requests.get(root_url+"client_id="+str(settings.APP_ID_FB)+"&client_secret="+settings.SECRET_KEY_FB+"&redirect_uri="+settings.REDIRECT_URI+"&code="+code)
            content = res.json()
            if "error" in content:
                error = content
                raise ValueError
            request_url ="https://graph.facebook.com/me?fields=first_name,last_name,birthday,gender&access_token="+content["access_token"]
            info = requests.get(request_url)
            request_url = "https://graph.facebook.com/v3.3/me/picture?type=large&redirect=false&access_token="+content["access_token"]
            photo = requests.get(request_url)
            info = info.json()
            photo = photo.json()
            info.update(photo)

            id = info["id"]
            if len(User.objects.filter(email = str(id))) == 0:
                data = {
                    "id": {
                        "email": str(id),
                        "firstName": info["first_name"],
                        "lastName": info["last_name"],
                        "role": User.PARTICIPANT,
                        "password": uuid.uuid4().hex,
                        "photo": info["data"]["url"]
                    }
                }
                serializer = ParticipantSerializer(data = data)
                serializer.is_valid(raise_exception=False)
                serializer.save()
                user = User.objects.get(email = str(id))
                user.is_social = True
                user.save()
            else:
                user = User.objects.get(email = str(id))
            res = {}
            res['id'] = "%s" % (user.id)
            res['email'] = "%s" % (user.email)
            res['firstName'] = "%s" % (user.firstName)
            res['lastName'] = "%s" % (user.lastName)
            res['role'] = "%s" % (user.role)
            res['photo'] = "%s" % (user.photo)
            res["jwt"] = getJWT(user)
            res["social"] = "fb"
            if len(user.participant.passedTests.all())==3:
                res['test'] = True
            return Response(data = res, status=status.HTTP_201_CREATED)


            return Response(info, status=status.HTTP_200_OK)
        except ValueError:
            res = error
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        except:
            raise
            res = {'error': 'Неизвестная ошибка'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

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
                    if '/' not in res["id"]["photo"]:
                        res["id"]["photo"] = "https://digitalnsk.ru:8000/media/"+res["id"]["photo"]

                return Response(data = res, status = status.HTTP_200_OK)
            else:
                serializer = UserSerializer(user)
                res = {}
                data = serializer.data
                res.update(data)
                return Response(data = data, status = status.HTTP_200_OK)
        
        except User.DoesNotExist:
            res = {"error": "Такого пользователя не существует"}
            return Response(data = res, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
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
            try:
                updateInfo = json.loads(request.body.decode("utf-8"))
            except:
                if "data" in request.data:
                    updateInfo = request.data["data"]
                elif "data" in request.POST:
                    updateInfo = request.POST.get("data")
                if type(updateInfo) == str:
                    updateInfo = json.loads(updateInfo)
            try:
                updateInfo["id"].pop("email")
            except:
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
                if "photo" in request.FILES:
                    fl = True
                    bphoto = request.FILES.get("photo", b"no photo").read()
                    photo_dir = settings.MEDIA_ROOT+"/other_roles/"
                    while True:
                        photo = uuid.uuid4().hex
                        if photo not in os.listdir(photo_dir):
                            break
                    f = open(photo_dir+photo, mode = 'wb')
                    f.write(bphoto)
                    f.close()
                    try:
                        updateInfo["photo"] = "https://digitalnsk.ru/media/other_roles/"+photo
                    except:
                        updateInfo = json.loads(updateInfo.read())
                        updateInfo["photo"] = "https://digitalnsk.ru/media/other_roles/"+photo
                if "password" in updateInfo:
                    UserSerializer.update_password(UserSerializer, instance = user, old_password = updateInfo["password"][0], password = updateInfo["password"][1])
                    updateInfo.pop("password")
                serializer = UserSerializer(user, updateInfo, partial = True)
                serializer.is_valid(raise_exception = True)
                serializer.save()
                data = serializer.data
                res = {"jwt": getJWT(user)}
                res.update(data)

                return Response(data = res, status = status.HTTP_200_OK)

        except User.DoesNotExist as e:
            raise(e)
            res = {"error": "Такого пользователя не существует"}
            return Response(data = res, status = status.HTTP_404_NOT_FOUND)
        except ValueError:
            res = {"error": "Пароли не совпадают"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise e
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

class TutorList(APIView):
    """Получение списка тьюторов"""
    permission_classes = (AllowAny,)

    def get(self, request):
        """Попрвить чтобы мог поучить только админ"""
        try:
            tutors = User.objects.filter(role = User.TUTOR)
            res = {"tutors": []}
            for tutor in tutors:
                serializer = UserSerializer(tutor)
                res["tutors"].append(serializer.data)
            return Response(data = res, status = status.HTTP_200_OK)

        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            id = request.META["HTTP_ID"]
            admin = User.objects.get(id = id)
            if admin.role == User.ADMINISTRATOR:
                if "email" in data:
                    user = User.objects.get(email = data["email"])
                    if user.role == User.TUTOR:
                        user.delete()
                        return Response(status = status.HTTP_204_NO_CONTENT)
                    else:
                        res = {"error": "It's not tutor"}
                        return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
                else:
                    res = {"error": "Wrong data"}
                    return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            else:
                res = {"error": "Permission denied"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        except:
            res = {"error": "Unknown error"}
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
                if '/' in user.photo:
                    res = {"photo": user.photo}
                else:
                    res = {"photo": "https://digitalnsk.ru:8000/media/"+user.photo}
            else:
                res = {"photo": None}
            return Response(data = res, status = status.HTTP_200_OK)
        except Exception as e:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)


class FeedBack(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            send_feedback_msg(data["name"], data["email"], data["msg"])
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

class FalseSignUp(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        path = os.path.join(settings.MEDIA_ROOT,"list.xlsx")
        book = openpyxl.load_workbook(filename = path)
        sheet = book["list"]
        sheet['F1'] = "e-mail"
        sheet['G1'] = "пароль"
        data = {
            "id": {
                "email": "",
                "firstName": "",
                "lastName": "",
                "patronymic": "",
                "password": "",
                "role": User.PARTICIPANT,
                "emailConfirmed": True
            },
            "eduInstitution":  "",
            "level": "",
        }
        email = uuid.uuid4().hex[:10] + "@digitalnsk.ru"
        password = uuid.uuid4().hex[:10]
        sheet['F7001'] = email
        sheet['G7001'] = password
        data["id"]["email"] = email
        data["id"]["firstName"] = sheet['B7001'].value
        data["id"]["lastName"] = sheet['A7001'].value
        data["id"]["patronymic"] = sheet['C7001'].value
        data["id"]["password"] = password
        data["eduInstitution"] = str(sheet['D7001'].value)
        data["level"] = str(sheet['E7001'].value) + " класс"

        serializer = ParticipantSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(data)
        book.save(path)
        return Response(status=status.HTTP_204_NO_CONTENT)