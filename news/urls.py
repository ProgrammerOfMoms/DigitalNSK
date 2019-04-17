from django.urls import path, re_path, include


from news.views import *


urlpatterns = [
    path("add/", News.as_view()),
]