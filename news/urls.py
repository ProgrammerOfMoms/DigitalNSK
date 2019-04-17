from django.urls import path, re_path, include


from news.views import *


urlpatterns = [
    path("add/", NewsView.as_view()),
]