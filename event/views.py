from django.shortcuts import render
from django.core.mail import send_mail
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
            events = user.events.all()
            for event in events:
                data.append(EventSerializer(event).data)
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
                if event.partiсipants < event.max_partiсipants:
                    event.partiсipants = event.partiсipants + 1
                    event.save()
                    if event not in user.events.all():
                        event.participant.add(user)
                        return Response(status = status.HTTP_200_OK)
                    else:
                        return Response(data = {"error": "Пользователь уже учавствует в данном мероприятии"}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data = {"error": "Много участников"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            if "event" in data:
                event_id = data["event"]
                user = Participant.objects.get(id = id)
                event = Event.objects.get(id = event_id)
                if event.partiсipants > 0:
                    event.partiсipants = event.partiсipants - 1
                    event.save()
                    if event in user.events.all():
                        event.participant.remove(user)
                        return Response(status = status.HTTP_200_OK)
                    else:
                        return Response(data = {"error": "Пользователь не учавствует в данном мероприятии"}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data = {"error": "Пользователь не учавствует в данном мероприятии"}, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

class EventInfo(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            if "event" in request.GET:
                user = Participant.objects.get(id = id)
                event_id = request.GET["event"]
                event = Event.objects.get(id = event_id)
                res = EventSerializer(event)
                data = res.data
                if event in user.events.all():
                    flag = True
                else:
                    flag = False
                res = {"id": data, "register": flag}
                res.update(data)
                return Response(data = res, status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

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
                    if item.name != "Базовая компетенция":
                        temp = {"competence": item.name, "subCompetencies": data1[item.name]}
                        data.append(temp)
                    else:
                        temp = {"competence": item.name, "subCompetencies": data2}
                        data.append(temp)
                res = {"Competencies": data}
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
        length = len(users)
        sheet['A1'] = "№"
        sheet['B1'] = "Имя"
        sheet['C1'] = "Фамилия"
        sheet['D1'] = "Отчество"
        sheet['E1'] = "Учебное заведение"
        sheet['F1'] = "Класс/курс"
        sheet['G1'] = "Телефон"
        sheet['H1'] = "Почта"
        sheet['I1'] = "Компетенция"
        sheet['J1'] = "Баллы"
        sheet['K1'] = "Базовые компетенции"
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
                sheet['G' + i] = person.phoneNumber
                sheet['H' + i] = person.email
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
                sheet['K' + i] = listComp
                if  comp == None:
                    sheet['I' + i] = "Нет кометенции"
                else:
                    sheet['I' + i] = comp.name
                    try:
                        sheet['J' + i] = user.points
                    except:
                        sheet['J' + i] = 0
                index = index + 1
        send_mail(  subject = 'Загрузка прошла успешно',
                message = "Кол-во участников: " + str(length),
                from_email = 'sibtiger.nsk@gmail.com',
                recipient_list = ['drestbm@gmail.com'],
                fail_silently=False)
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

    def post(self, request):
        import threading
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                threading.Thread(target=self.formXSLX).start()
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

class Func(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = User.objects.get(id = id)
            if user.role == User.ADMINISTRATOR:
                events = Event.objects.all()
                for event in events:
                    event.mainComp = event.mainCompetence.all()[0]
                    event.save()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "В доступе отказано"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)

class EventParticipants(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        pass
    #     if "HTTP_ID" in request.META:
    #         id = request.META["HTTP_ID"]
    #         user = User.objects.get(id = id)
    #         if user.role == User.ADMINISTRATOR:
    #             if "event" in request.GET:
    #             event = Event.objects.get(id = request.GET["event"])
    #             participants = event.participant.all()
    #             data = {"list": []}
    #             for item in participants:
    #                 data["list"].append(item)
    #         else:
    #             return Response(data = {"error": "В доступе отказано"}, status = status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(data = {"error": "Отсутствует id пользователя"}, status = status.HTTP_400_BAD_REQUEST)