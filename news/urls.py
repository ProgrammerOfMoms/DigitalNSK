from django.urls import path, re_path, include


from news.views import *


urlpatterns = [
    path("req/", NewsView.as_view()),
]