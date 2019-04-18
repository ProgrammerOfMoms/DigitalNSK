from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from news.serialize import NewsSerializer
from news.models import News
from DigitalNSK import settings


import json
import copy
import datetime
import base64
import os
import uuid
import random




class NewsView(APIView):
    
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            html_code = request.POST.get("html_code").decode("utf-8")
            title = request.POST.get("title").decode("utf-8")
            print(html_code, title)
            
            bphoto = request.FILES.get("photo", b"no photo").read()
            photo_dir = settings.MEDIA_ROOT+"/news/"
            while True:
                photo = uuid.uuid4().hex
                if photo not in os.listdir(photo_dir):
                    break
            f = open(photo_dir+photo, mode = 'wb')
            f.write(bphoto)
            f.close()
            data = {"html_code": html_code, "photo": "https://digitalnsk.ru/media/news/"+photo, "title": title}
            serializer = NewsSerializer(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            d = serializer.data
            data["id"] = d["id"]
            data["date"] = d["date"]

            return Response(data = data, status = status.HTTP_201_CREATED)
        except Exception as e:
            raise(e)
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            if "id" in request.GET:
                id = request.GET["id"]
                news = News.objects.get(id = id)
                serializer = NewsSerializer(news)
                data = {
                        "id": serializer.data["id"],
                        "title": serializer.data["title"],
                        "html_code": serializer.data["html_code"],
                        "photo": "https://digitalnsk.ru/media/news/"+serializer.data["photo"],
                        "date": serializer.data["date"]}
                return Response(data = data, status = status.HTTP_200_OK)
            else:
                news = News.objects.all()
                data = {"news": []}
                for item in news:
                    data["news"].append({
                        "id": item.id,
                        "title": item.title,
                        "html_code": item.html_code,
                        "photo": "https://digitalnsk.ru/media/news/"+item.photo,
                        "date": item.date})
                return Response(data = data, status = status.HTTP_200_OK)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)



