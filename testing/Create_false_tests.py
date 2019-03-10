from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serialize import *
import json

def create_false_test(request):
    test = json.loads(request.body.decode("utf-8"))
    serializer = TestSerializer(data = test)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    res = 1
    return Response(res, status=status.HTTP_200_OK)