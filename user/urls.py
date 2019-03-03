from django.urls import path, re_path, include


from .views import *

urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('signin/', SignIn.as_view()),
    path('get/', Profile.as_view()),
]