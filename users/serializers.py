from abc import ABC

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth.models import User


# Create your models here.

class CreateUserSerializer(serializers.ModelSerializer):
    # validated_data contain all input data
    # This is used for password encryption where user enter password while sign up
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class UserProfileViewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserProfileViewSerializer()

    class Meta:
        model = UserProfile
        fields = ('default_pic_url', 'bio', 'user', 'created_on', 'last_update',)
