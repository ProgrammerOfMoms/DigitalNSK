from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from DigitalNSK import settings

from .models import *
from .serialize import UserSerializer


class SignUp(APIView):
    """Регистрация через email и password"""

    permission_classes = (AllowAny,)
 
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SignIn(APIView):
    """Авторизация через email и password"""

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
    
            user = User.objects.get(email=email, password=password)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['firstName'] = "%s" % (user.firstName)
                    user_details['lastName'] = "%s" % (user.lastName)
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__, request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
    
                except Exception as e:
                    raise e
            else:
                res = {'error': 'Пользователь не найден'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'Пожалуйста, введите email и пароль'}
            return Response(res)
            
        except User.DoesNotExist:
            res = {'error': 'Пользователь не найден'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
