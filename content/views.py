from django.shortcuts import render
from .models import UserPost, PostMedia
from .serializers import UserPostCreateSerializer, PostMediaCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
from rest_framework import generics
from rest_framework import mixins


class UserPostCreateFeed(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def post(self, request, *args, **kwargs):
        # request.data['current_user'] = request.user.profile #This is alternate ways of line no 16 in
        # get_serializer_context
        return self.create(request, *args, **kwargs)


class PostMediaView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = PostMedia.objects.all()
    serializer_class = PostMediaCreateSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
