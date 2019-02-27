from django.urls import path, include

from .views import *

urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('signin/', SignIn.as_view()),
]