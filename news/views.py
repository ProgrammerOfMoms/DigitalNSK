from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated


import json
import copy
import datetime



# class News(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#             serializer = 


#         except:
#             pass


