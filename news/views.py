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
            html_code = request.POST.get("html_code")
            title = request.POST.get("title")

            
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
                        "photo": serializer.data["photo"],
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
                        "photo": item.photo,
                        "date": item.date})
                return Response(data = data, status = status.HTTP_200_OK)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            if "id" in data:
                news = News.objects.get(id = data["id"])
                news.delete()
                return Response(status = status.HTTP_204_NO_CONTENT)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            if "data" in request.data:
                updateInfo = request.data["data"]
            if type(updateInfo) == str:
                updateInfo = json.loads(updateInfo)
            if "photo" in request.FILES:
                bphoto = request.FILES.get("photo", b"no photo").read()
                photo_dir = settings.MEDIA_ROOT+"/news/"
            
                news = News.objects.get(id = updateInfo["id"])
                old_photo = news.photo
                if old_photo != "":
                    start = old_photo.find('_')
                    if start == -1:
                        new_photo = old_photo + "_1"
                    else:
                        prefix = old_photo[start+1:]
                        prefix = str(int(prefix)+1)
                        new_photo = old_photo[:start]+"_"+prefix
                else:
                    while True:
                        new_photo = uuid.uuid4().hex
                        if new_photo not in os.listdir(photo_dir):
                            break
                            
                f = open(photo_dir+new_photo, mode = 'wb')
                f.write(bphoto)
                f.close()

                data = {"photo": "https://digitalnsk.ru/media/news/"+new_photo}
                serializer = NewsSerializer(news, data, partial = True)
                serializer.is_valid(raise_exception = True)
                serializer.save()

            if updateInfo:
                
                # if "html_code" in updateInfo:
                #     html_code = updateInfo["html_code"]
                # if "title" in updateInfo:
                #     title = updateInfo["title"]

                # if html_code and title:
                #     data = {"html_code": html_code, "title": title}
                # elif html_code:
                #     data = {"html_code": html_code}
                # else:
                #     data = {"title": title}

                news = News.objects.get(id = updateInfo["id"])

                serializer = NewsSerializer(news, updateInfo, partial = True)
                serializer.is_valid(raise_exception = True)
                serializer.save()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except:
            res = {"error": "Неизвестная ошибка"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)




