from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from news.serialize import NewsSerializer
from DigitalNSK import settings


import json
import copy
import datetime
import base64
import os
import uuid
import random




class News(APIView):
    
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            html_code = request.FILES["html_code"].read().decode("utf-8")
            
            bphoto = request.FILES["photo"].read()
            photo_dir = settings.MEDIA_ROOT+"/news/"
            while True:
                photo = uuid.uuid4().hex
                if photo not in os.listdir(photo_dir):
                    break
            f = open(photo_dir+photo, mode = 'wb')
            f.write(bphoto)
            f.close()
            data = {"html_code": html_code, "photo": photo}
            serializer = NewsSerializer(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            d = serializer.data
            data["id"] = d["id"]
            data["date"] = d["date"]

            return Response(data = data, status = status.HTTP_201_CREATED)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            if "id" in request.GET:
                print("tut")
                id = request.GET["id"]
                print(id)
                # news = News.objects.get(id = id)
                # print(news)
                # # serializer = NewsSerializer(news)
                # # print(serializer)
                return Response(data = {}, status = status.HTTP_200_OK)
            else:
                print("ttt")
        except:
            pass



