from rest_framework import serializers
from .models import InfoBlock, bracelet,Profile
from django.db import models

class InfoBlockDeleteSerializer(serializers.ModelSerializer):
    """ID блока"""
    class Meta:
        model = InfoBlock
        fields = ('id',)


class InfoBlockDetailSerializer(serializers.ModelSerializer):
    """Один инфоблок"""
    class Meta:
        model = InfoBlock
        fields = ('id', 'title', 'content')


class InfoBlockCreateSerializer(serializers.ModelSerializer):
    """Содержание блока"""
    class Meta:
        model = InfoBlock
        fields = ('title', 'content')


class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = bracelet
        fields = ('is_activated',)

class CreateBraceletSerializers(serializers.ModelSerializer):
    class Meta:
        model = bracelet
        fields = ('profile_id', 'id', 'unique_code',  'is_activated')


class JoinBraceletSerializers(serializers.ModelSerializer):

    class Meta:
        model = bracelet
        fields = ('unique_code',)

class CheckCodeSerializers(serializers.ModelSerializer):
    unique_code = models.CharField(max_length=6,)
    class Meta:
        model = bracelet

class ProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user',)


class ProfileViewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user',)