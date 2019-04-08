from django.urls import path, re_path, include

from .views import *

urlpatterns = [
    path('', SpaceOfSample.as_view()),
    path('signup/', SignUpEvent.as_view())
]