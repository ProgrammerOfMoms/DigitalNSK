from django.urls import path, re_path, include

from .views import *
from .Create_false_tests import create_false_test

urlpatterns = [
    path('test1/', test1),
    path('test2/', test2),
    path('additional/', additional),
    path('add-question/', test11),
]