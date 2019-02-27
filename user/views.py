from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import *


class SignUp(APIView):

    def post(self, request):
        pass
    
    def get(self, request):
        pass