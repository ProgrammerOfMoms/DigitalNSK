from django.urls import path, re_path, include

from .views import *


urlpatterns = [
    path('tests/', Testing.as_view()),
    path('ger/', func.as_view())
]