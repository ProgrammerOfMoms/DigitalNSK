from django.urls import path, re_path, include

from .views import *
from .Create_false_tests import create_false_test

urlpatterns = [

    path('test1/', Test1),
    path('test2/', Test2),
    #path('test3/', falseTest3.as_view()),
]