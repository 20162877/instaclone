from rest_framework import serializers
from .models import Users, UserProfile
from django.contrib.auth.hashers import make_password
# Create your models here.


class CreateUserSerializer(serializers.ModelSerializer):
    # validated_data contain all input data
    # This is used for password encryption where user enter password while sign up
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        user = Users.objects.create(**validated_data)
        UserProfile.objects.create(user=user)
        Users.

        return user

    class Meta:
        model = Users
        fields = ('name', 'password', 'email', 'phone_number', )
