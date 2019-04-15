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
                data = []
                for event in events:
                    data.append(EventSerializer(event).data)
                res = {"list": data}
                return Response(data = res, status = status.HTTP_200_OK)
            else:
                if "date" in request.GET:
                    user = Participant.objects.get(id = id)
                    events = Event.objects.filter(date = request.GET["date"])
                    userEvents = user.events.all()
                    competence = user.mainCompetence
                    data = []
                    for event in events:
                        if event not in userEvents and competence in event.mainCompetence.all():
                            data.append(EventSerializer(event).data)
                            break                            
                    res = {"list": data}
                    return Response(data = res, status = status.HTTP_200_OK)
                else:
                    return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

class SignUpEvent(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if "HTTP_ID" in request.META:
            data = []
            id = request.META["HTTP_ID"]
            user = Participant.objects.get(id = id)
            progresses = user.events.all()
            for  progress in progresses:
                data.append(EventSerializer(progress.event).data)
            res = {"list": data}
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

    def get(self, request):
        if "event" in request.GET:
            event_id = request.GET["event"]
            event = Event.objects.get(id = event_id)
            res = EventSerializer(event)
            data = res.data
            res = {"id": data}
            res.update(data)
            return Response(data = res, status = status.HTTP_200_OK)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)

#Администратор
class EventAdd(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                main = MainCompetence.objects.filter(isBase = False)
                mas = SideCompetence.objects.all()
                data1 = {}
                for item in main:
                    data1[item.name] = []
                data2 = []
                for item in mas:
                    temp = item.overCompetence.overCompetence
                    if temp.isBase == True:
                        data2.append(item.name)
                    else:
                        data1[temp.name].append(item.name)
                data = []
                for item in main:
                    temp = {"competence": item.name, "subCompetencies": data1[item.name]}
                    data.append(temp)
                res = {"mainCompetencies": data, "baseCompetencies": data2}
                return Response(data = res, status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "В доступе отказано"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                serializer = EventSerializer(data = data)
                serializer.is_valid(raise_exception = True)
                serializer.save()
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
        sheet['I1'] = "Базовые компетенции"
        index = 2
        for user in users:
            if (user.id_id > 400):
                person = user.id
                i = str(index)
                comp = user.mainCompetence
                sheet['A' + i] = index - 1
                sheet['B' + i] = person.firstName
                sheet['C' + i] = person.lastName
                sheet['D' + i] = person.patronymic
                sheet['E' + i] = user.eduInstitution
                sheet['F' + i] = user.level
                try:
                    listComp = ""
                    res = eval(user.passedTests.get(test = Test.objects.get(mode = 1)).competence)
                    types = res["types"]
                    values = res["values"]
                    k = 0
                    for type in types:
                        if values[k] == 1:
                            listComp = listComp + type + ", "
                        k = k + 1
                except:
                    listComp = "Нет компетенций"
                if listComp == "":
                    listComp = "Нет компетенций"
                sheet['I' + i] = listComp
                if  comp == None:
                    sheet['G' + i] = "Нет кометенции"
                else:
                    sheet['G' + i] = comp.name
                    try:
                        res = user.passedTests.get(test = Test.objects.get(name = comp.name)).competence
                        sheet['H' + i] = int(eval(res)["result"])
                    except:
                        sheet['H' + i] = 0
                index = index + 1
            book.save(path)

    # def error(self):
    #     users = Participant.objects.all()
    #     res = []
    #     for user in users:
    #         try:
    #             if len(user.passedTests.filter(test = Test.objects.get(name = user.competence.name))) > 1:
    #                 res.append(user.id_id)
    #         except:
    #             print(1)
    #     print(res)

    def get(self, request):
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                self.formXSLX()
                #self.error()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "В доступе отказано"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

class EventEdit(APIView):
    permission_classes = (AllowAny,)

    def delete(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                if "event" in data:
                    try:
                        Event.objects.filter(id = data["event"]).delete()
                    except:
                        return Response(data = {"error": "Мероприятия не существует"}, status = status.HTTP_400_BAD_REQUEST)
                    return Response(status = status.HTTP_200_OK)
                else:
                    return Response(data = {"error": "Нет нужных полей"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data = {"error": "В доступе отказано"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)
