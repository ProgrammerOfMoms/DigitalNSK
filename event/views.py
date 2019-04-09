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
from DigitalNSK import settings
from .models import *
from user.models import *
from .serialize import *

import json
# Create your views here.
class SpaceOfSample(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        flag = True 
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            if "date" in request.GET:
                user = Participant.objects.get(id = id)
                events = Event.objects.filter(date = request.GET["date"], competence = user.competence)
            res = []
            progresses = user.events.all()
            print(events)
            for event in events:
                for  progress in progresses:
                    if progress.event == event:
                        flag = False
                if flag:
                    res.append(EventSerializer(event).data)
            return Response(data = res, status = status.HTTP_200_OK)

class SignUpEvent(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            if "event" in data:
                event_id = data["event"]
                user = Participant.objects.get(id = id)
                event = Event.objects.get(id = event_id)
                if len(user.events.filter(event = event)) == 0:
                    progress = Progress.objects.create(progress = -1, event = event)
                    user.events.add(progress)
                    return Response(status = status.HTTP_200_OK)
                else:
                    return Response(data = {"error": "Пользователь уже учавствует в данном мероприятии"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)


class EventFunc(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            if "event" in data:
                event_id = data["event"]
                event = Event.objects.get(id = event_id)
                res = EventSerializer(event)
                return Response(data = res.data, status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)