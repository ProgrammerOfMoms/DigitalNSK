from django.urls import path, re_path, include


from user.views import *


urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('signin/', SignIn.as_view()),
    path('info/', Profile.as_view()),
    path('recovery-password/', PasswordRecovery.as_view()),
    path('confirm-email/', ConfirmEmail.as_view()),
    path('upload-photo/', UploadPhoto.as_view()),
    path('tutors/', TutorList.as_view()),
    path('feedback/', FeedBack.as_view()),
    path('test/', TestClass.as_view()),
    path('vk-sign-in/', VKSignIn.as_view()),
    path('fb-sign-in/', FaceBookSignIn.as_view()),
    #path('false/', FalseSignUp.as_view()),
]