from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
import json

class falseTest1(APIView):

    def get(self, request):
        try:
            res = Test.objects.get(id = 1)
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            mas = [0,0]
            data = json.loads(request.body.decode("utf-8"))
            if "answers" in data:
                for answer in data["answers"]:
                    mas[answer] = mas[answer] + 1
                if mas[0] > mas[1]:
                    res = 0
                else:
                    res = 1
                return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class falseTest2(APIView):

    def get(self, request):
        try:
            res = Test.objects.get(id = 2)
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
            try:
                mas = [0,0,0,0,0]
                data = json.loads(request.body.decode("utf-8"))
                if "answers" in data:
                    for answer in data["answers"]:
                        mas[answer-1] = mas[answer-1] + 1
                    max = mas[0]
                    maxI = 0
                    for i in range(1,5):
                        if mas[i] > max:
                            max = mas[i]
                            maxI = i
                    res = maxI + 1
                    return Response(res, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
"""
class falseTest3(APIView):

    def get(self, request):
"""