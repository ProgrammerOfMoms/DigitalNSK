from django.urls import path, re_path, include

from .views import *
from .Create_false_tests import create_false_test

urlpatterns = [
    path('', create_false_test),
    path('test1/', falseTest1.as_view()),
    path('test2/', falseTest2.as_view()),
    #path('test3/', falseTest3.as_view()),
]