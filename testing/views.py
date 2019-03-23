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

def test1(data, user):
    if "answers" in data:
        test = Test.objects.get(mode = 1)
        temp = test.groups.exclude(name = "Ничего")
        types = []
        for _type in temp:
            types.append(_type.name)
        length = len(types)
        val = [0] * length
        for answer in data["answers"]:
            group = Group.objects.get(id = answer).key - 1
            if group < length:
                val[group] = val[group] + 1
        res = {
            "status": True,
            "types": types,
            "values": val
        }
        result = ResultOfTest.objects.create(competence = str(res), test = test)
        user.passedTests.add(result)
    else:
        res = {"error": "Отсутствуют необходимые поля"}
    return res

def test2(data, user):
    if "answers" in data:
        answers = data["answers"]
        test = Test.objects.get(mode = 2)
        groups = test.groups.all()
        nameOfGroups = []
        val = [0] * len(groups)
        for group in groups:
            nameOfGroups.append(group.name)
        for answer in data["answers"]:
            val[answer-1] = val[answer-1] + 1

        maximum = max(val)
        maxI = val.index(maximum)
        if val.count(maximum) == 1:
            res = {
                "additional": False,
                "types": nameOfGroups,
                "values": val
            }
            result = ResultOfTest.objects.create(competence = str(res), test = test)
            user.passedTests.add(result)
        else:
            types = [maxI]
            for  i in range(maxI+1,len(groups)):
                if maximum == val[i]:
                    types.append(i)
            addQuestion = test.additionalQuestion
            mas = []
            answers = addQuestion.answers.all()
            for item in types:
                group = {
                    "types": answers[item].content,
                    "group": answers[item].group.id
                }
                mas.append(group)
                print(mas)
            res = {
                "additional": True,
                "values": val,
                "types": nameOfGroups,
                "description": addQuestion.content,
                "questions": mas
            }
    else:
        res = {"error": "Отсутствуют необходимые поля"}
    return res

def test0(data, user):
    if "values" in data and "types" in data and "answer" in data:
        Group.objects.get(id = data["answer"])


def test3(data, user):
        try:
            if "answers" in data:
                id = data["id"] 
                test = Test.objects.get(id = id)
                sum = 0
                for answer in data["answers"]:
                    sum = sum + answer
                res = {"result": sum * 5 / len(data["answers"])}
                result = ResultOfTest.objects.create(competence = str(res), test = test)
                user.passedTests.add(result)
                
            else:
                res = {"error": "Отсутствуют необходимые поля"}
            return res
        except:
            res = {"error": "Что-то пошло не так"}
            return res

class Testing(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        #try:
            if "HTTP_ID" in request.META:
                id = request.META["HTTP_ID"]
                _type = request.GET["type"]
                user = Participant.objects.get(id = id)
                #if len(user.passedTests.all()) < int(_type):
                if _type != "3":
                    test = Test.objects.get(mode = _type)
                    serializer = TestSerializer(test)
                    data = serializer.data
                    res = {"id": data["id"]}
                    data.pop("id")
                    res.update(data)
                else:
                    test2 = Test.objects.get(mode = 2)
                    print(user.passedTests.get(test = test2))
                    temp = user.passedTests.get(test = test2).competence
                    result = eval(temp)
                    val = result["values"]
                    types = result["types"]
                    test = Test.objects.get(name = types[val.index(max(val))])
                    serializer = TestSerializer(test)
                    data = serializer.data
                    res = {"id": data["id"]}
                    data.pop("id")
                    res.update(data)
                return Response(data = res, status = status.HTTP_200_OK)
                #else:
                #    res = {"error": "Не указан id пользователя"}
                #    return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            else:
                res = {"error": "Не указан id пользователя"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        #except:
        #    res = {"error": "Неизвестная ошибка"}
        #    return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        data = json.loads(request.body.decode("utf-8"))
        if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            if "type" in data:
                #try:
                    user = Participant.objects.get(id = id)
                    if data["type"] == 1:
                        res = test1(data = data, user = user)
                        if "error" in res:
                            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(data = res, status = status.HTTP_200_OK)
                    elif data["type"] == 2:
                        res = test2(data = data, user = user)
                        if "error" in res:
                            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(data = res, status = status.HTTP_200_OK)
                    elif data["type"] == 3:
                        res = test3(data = data, user = user)
                        if "error" in res:
                            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(data = res, status = status.HTTP_200_OK)
                    if data["type"] == 0:
                        res = test0(data = data, user = user)
                        if "error" in res:
                            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(data = res, status = status.HTTP_200_OK)
                    else:
                        res = {"error": "Неизвестный тип теста"}
                        return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
                #except:
                #    res = {"error": "Такого пользователя не существует"}
                #    return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            else:
                res = {"error": "Не указан тип теста"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        else:
            res = {"error": "Не указан id пользователя"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
            
