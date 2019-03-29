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
         if "HTTP_ID" in request.META:
            id = request.META["HTTP_ID"]
            user = Participant.objects.get(id = id)
            events = Event.objects.filter(competence = user.competence)
            res = []
            for event in events:
                res.append(EventSerializer(event).data)
            return Response(data = res, status = status.HTTP_200_OK)