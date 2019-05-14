from django.urls import path, re_path, include

from .views import *


urlpatterns = [
    path('test/', Testing.as_view()),
    path('ger/', func.as_view())
]