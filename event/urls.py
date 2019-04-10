from django.urls import path, re_path, include

from .views import *

urlpatterns = [
    path('', EventList.as_view()),
    path('signup/', SignUpEvent.as_view()),
    path('event/', EventInfo.as_view())
]