from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.db import models
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from myauth.models import User
from .serializers import *


class AccountDefinition(APIView):
    @permission_classes([AllowAny])
    def get(self, request, pk):
        try:
            profile = codeHandler.objects.get(id=pk)
            if profile.is_activated:
                return Response(profile.unique_code)
            else:
                return Response({'status': 'get token'})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @permission_classes([AllowAny])
    def post(self, request, pk):
        try:
            profile = codeHandler.objects.get(unique_code=request.data.get('unique_code'))
            if profile.profile_id:
                return Response(data={"profile_id": profile.profile_id}, status=status.HTTP_200_OK)
            return Response(status=404)

        except:
            return Response(status=404)


@permission_classes([IsAuthenticated])
class JoinHandler(APIView):
    def post(self, request, pk):
        unique_handler = codeHandler.objects.get(id=pk)
        serializer = JoinHandlerSerializers(unique_handler)
        code = request.data.get('unique_code')
        if code:
            if code == serializer.data.get('unique_code'):
                user_id = request.user.id
                unique_handler.profile_id = user_id
                unique_handler.is_activated = True
                unique_handler.save()
                return Response({"status": "Connected"})
            else:
                return Response({"status": "Error"})
        else:
            return Response({"status": "Data Error"})


class createhandler(APIView):
    @permission_classes([IsAdminUser])
    def post(self, request):
        try:
            handler = CreateHandlerSerializers(data=request.data.get())
            if handler.is_valid():
                handler.save()
                return Response(status=201)
            else:
                return Response(status=400)
        except:
            return Response(status=404)


class deleteHandler(APIView):
    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        try:
            handler = codeHandler.objects.get(pk=pk)
            handler.delete()
            return Response(status=201)
        except:
            return Response(status=404)

# class HandlerCreateView(APIView):

# @permission_classes([IsAuthenticated])
# class JoiningHandler(APIView):
#     def post(self, request,pk):
#         unique_code= codeHandler.objects.get(pk=pk)
#         serializer = JoinHandlerSerializers(unique_code)
#         check_unique_code = JoinHandlerSerializers(data=request.data)
#         response_data = User.objects.get(pk=pk)
#         serializerprofile = JoinAccountSerializers(response_data)
#
#         if serializer==check_unique_code: return
