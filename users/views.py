from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserProfile
from .serializers import CreateUserSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


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
