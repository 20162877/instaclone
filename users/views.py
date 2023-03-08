from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserProfile, NetworkEdge
from .serializers import CreateUserSerializer, UserProfileSerializer, UpdateUserProfileSerializer, \
    NetworkEdgeCreationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, \
    RetrieveModelMixin
from rest_framework.generics import GenericAPIView


@api_view(['POST'])
def create_user(request):
    # request.data
    # Serialization Creating python object -> native data type -> into JSON/xml # Representing data
    # deserialization - JSON INPUT -> native data type -> db rows  # creating data
    # user = Users()
    # name = request.data['name']
    # email = request.data['email']
    # number = request.data['phone_number']
    # user.save()
    print("Request data --> ", request.data)
    serializer = CreateUserSerializer(data=request.data)
    response_data = {
        'error': None,
        'data': None
    }
    if serializer.is_valid():
        user = serializer.save()  # save to user db
        refresh = RefreshToken.for_user(user)

        response_data['data'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        response_status = status.HTTP_200_OK
    else:
        response_data['error'] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_status)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  # Not allowed for anonymous user
def user_list(request):
    print("Request User -> ", request.user)
    print('Fetching all users from user profile')
    user = UserProfile.objects.all()  # Fetch all records from Userprofile table
    print("Done")
    serialized_data = UserProfileSerializer(instance=user, many=True)  #
    return Response(serialized_data.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, pk):
    user = UserProfile.objects.filter(id=pk).first()  # first return none if records not found
    serialized_data = UserProfileSerializer(instance=user)  #
    if user:
        response = {
            'error': None,
            'data': serialized_data.data
        }
        response_status = status.HTTP_200_OK
    else:
        response = {
            'error': "User Does not exist",
            'data': None
        }
        response_status = status.HTTP_400_BAD_REQUEST
    return Response(response, response_status)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    # UserProfile.object.filer(name=request.user)  related_name  ==== request.user.profile  Reverse relationship
    print("Request User --> ", request.data)
    print("Views --> 83")
    user_update_profile = UpdateUserProfileSerializer(instance=request.user.profile, data=request.data)
    print("Views --> 85")
    if user_update_profile.is_valid():
        user_profile = user_update_profile.save()
        response = {
            "data": UserProfileSerializer(instance=user_profile).data,
            "error": None
        }
        response_status = status.HTTP_200_OK
    else:
        response = {
            "data": user_update_profile.errors,
            "error": None
        }
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response, response_status)


class UserNetworkEdgeView(CreateModelMixin, GenericAPIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = NetworkEdge.objects.all()
    serializer_class = NetworkEdgeCreationSerializer

    def get(self, request):
        pass

    def post(self, request, *args, **kwargs): # To follow user
        print("Request --> ", request.data)
        print("request.user.profile.id --> ", request.user.profile.id )
        print("request.user.profile --> ", request.user.profile)
        print("request.user --> ", request.user)

        request.data['from_user'] = request.user.profile.id
        return self.create(request, *args, **kwargs)  # Saves request.data to NetworkEdge model

    def delete(self, request, *args, **kwargs): # To unfollow user
        # Token will give identity of user who is trying to unfollow
        # Id of the user being unfollowed can be supplied from body
        network_edge = NetworkEdge.objects.filter(from_user=request.user.profile, to_user=request.data['to_user'])
        if network_edge.exists():
            network_edge.delete()
            message = "User Unfollowed"
        else:
            message = "No edge found"
        return Response({'Data': None, 'message':message}, status=status.HTTP_200_OK)
