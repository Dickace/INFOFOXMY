from rest_framework import serializers
from .models import codeHandler
from django.db import models
from myauth.models import User

class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = codeHandler
        fields = ('is_activated',)

class CreateHandlerSerializers(serializers.ModelSerializer):
    class Meta:
        model = codeHandler
        fields = ('profile_id', 'id', 'unique_code',  'is_activated')


class JoinHandlerSerializers(serializers.ModelSerializer):

    class Meta:
        model = codeHandler
        fields = ('unique_code',)

class CheckCodeSerializers(serializers.ModelSerializer):
    unique_code = models.CharField(max_length=6,)
    class Meta:
        model = codeHandler
        fields = ('id',)

# class JoinAccountSerializers(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('connected_bracer',)