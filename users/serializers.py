from abc import ABC

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, UserProfile, NetworkEdge
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


class UserProfileViewSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=200)
    # first_name = serializers.CharField(max_length=200)
    # last_name = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', )


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserProfileViewSerializer()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('default_pic_url', 'bio', 'user', 'created_on', 'last_update', 'follower_count', 'following_count', )
        # exclude = ('id', 'is_verified')
    def get_follower_count(self,obj):
        return obj.follower.count()
    def get_following_count(self,obj):
        return obj.following.count()


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def update(self, instance, validated_data):  # instance refer to Model.UserProfile
        user = instance.user
        user.first_name = validated_data.pop('first_name', None)
        user.last_name = validated_data.pop('last_name', None)
        user.save()

        # instance.bio = validated_data.get('bio', None)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name')


class NetworkEdgeCreationSerializer(serializers.ModelSerializer):
    """
        Serializer Contains follow and follower
    """

    class Meta:
        model = NetworkEdge
        fields = ('from_user', 'to_user',)


class NetworkEdgeViewSerializer(serializers.ModelSerializer):
    from_user = UserProfileSerializer()
    to_user = UserProfileSerializer()

    class Meta:
        model = NetworkEdge
        fields = ('from_user', 'to_user', )