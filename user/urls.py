from django.urls import path, re_path, include


from .views import *


urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('signin/', SignIn.as_view()),
    path('info/', Profile.as_view()),
    path('recovery-password/', PasswordRecovery.as_view()),
]