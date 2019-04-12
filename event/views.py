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
from testing.models import Test

import json
# Create your views here.

#Пользователь
class EventList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        flag = True 
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            usr = User.objects.get(id = id)
            if usr.role == User.ADMINISTRATOR:
                events = Event.objects.all()
                return Response(data = events, status = status.HTTP_200_OK)
            else:
                if "date" in request.GET:
                    user = Participant.objects.get(id = id)
                    events = Event.objects.filter(date = request.GET["date"], competence = user.competence)
                    res = []
                    progresses = user.events.all()
                    for event in events:
                        for  progress in progresses:
                            if progress.event == event:
                                flag = False
                        if flag:
                            res.append(EventSerializer(event).data)
                    return Response(data = res, status = status.HTTP_200_OK)
                else:
                    return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

class SignUpEvent(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if "HTTP_ID" in request.META:
            res = []
            id = request.META["HTTP_ID"]
            user = Participant.objects.get(id = id)
            progresses = user.events.all()
            for  progress in progresses:
                res.append(EventSerializer(progress.event).data)
            return Response(data = res, status = status.HTTP_200_OK)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

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


class EventInfo(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if "event" in data:
            event_id = data["event"]
            event = Event.objects.get(id = event_id)
            res = EventSerializer(event)
            return Response(data = res.data, status = status.HTTP_200_OK)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)


#Администратор
class EventAdd(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                res = EventSerializer(data)
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "В доступе отказано"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)


class Excel(APIView):
    permission_classes = (AllowAny,)

    def formXSLX(self):
        import openpyxl, os, datetime
        date = str(datetime.datetime.now().date())
        path = os.path.join(settings.MEDIA_ROOT, "data.xlsx")
        try:
            book = openpyxl.load_workbook(filename = path)
        except:
            book = openpyxl.Workbook()
        try:
            sheet = book[date]
        except KeyError:
            sheet = book.create_sheet(date)
        users = Participant.objects.all()
        sheet['A1'] = "№"
        sheet['B1'] = "Имя"
        sheet['C1'] = "Фамилия"
        sheet['D1'] = "Отчество"
        sheet['E1'] = "Учебное заведение"
        sheet['F1'] = "Класс/курс"
        sheet['G1'] = "Компетенция"
        sheet['H1'] = "Баллы"
        index = 2
        for user in users:
            if (user.id.id > 400):
                i = str(index)
                sheet['A' + i] = index - 1
                sheet['B' + i] = user.id.firstName
                sheet['C' + i] = user.id.lastName
                sheet['D' + i] = user.id.patronymic
                sheet['E' + i] = user.eduInstitution
                sheet['F' + i] = user.level
                try:
                    sheet['G' + i] = user.competence.name
                    res = user.passedTests.get(test = Test.objects.get(name = user.competence.name)).competence
                    sheet['H' + i] = eval(res)["result"]
                except:
                    sheet['G' + i] = "Нет кометенции"
                index = index + 1
            book.save(path)

    def get(self, request):
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                self.formXSLX()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "В доступе отказано"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)