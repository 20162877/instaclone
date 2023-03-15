from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserProfile, NetworkEdge
from .serializers import CreateUserSerializer, UserProfileSerializer, UpdateUserProfileSerializer, \
    NetworkEdgeCreationSerializer, NetworkEdgeViewSerializer
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
    """ Get list of users """
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
    """ GEt user profile """
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
    """ Update User details such as First Name and Last Name """
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


class UserNetworkEdgeView(CreateModelMixin,
                          ListModelMixin,
                          GenericAPIView):
    """
    follow, unfollow and list of all follower.
    """
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = NetworkEdge.objects.all()
    serializer_class = NetworkEdgeCreationSerializer

    def get_serializer_class(self):
        """
        Uses NetworkEdgeViewSerializer class when get request is called
        """
        # Change the serializer in case follower are being requested.
        if self.request.method == 'GET':
            return NetworkEdgeViewSerializer
        return self.serializer_class
    
    def get_queryset(self):
        edge_direction = self.request.query_params['direction']
        # NetworkEdge.objects.all().filter(to_user=self.request.user.profile)
        print("Request --> ", self.request.user.profile)
        print("Request --> ", self.request.user)
        print("Request  ", self.request)
        if edge_direction == 'followers':
            return self.queryset.filter(to_user=self.request.user.profile)
        elif edge_direction == 'following':
            return self.queryset.filter(from_user=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        """
        List all follower of given user
        """
        print("request --> 143")
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        To follow user
        {
        to_user:2
        }
        request.user.profile.id(Token user) followed 2
        """
        # print("Request --> ", request.data)
        # print("request.user.profile.id --> ", request.user.profile.id)
        # print("request.user.profile --> ", request.user.profile)
        # print("request.user --> ", request.user)

        request.data['from_user'] = request.user.profile.id
        return self.create(request, *args, **kwargs)  # Saves request.data to NetworkEdge model

    def delete(self, request, *args, **kwargs):
        """
        Unfollow user
        {
        to_user:2
        }
        request.user.profile(token) unfollowed 2
        """
        # Token will give identity of user who is trying to unfollow
        # Id of the user being unfollowed can be supplied from body
        network_edge = NetworkEdge.objects.filter(from_user=request.user.profile, to_user=request.data['to_user'])
        if network_edge.exists():
            network_edge.delete()
            message = "User Unfollowed"
        else:
            message = "No edge found"
        return Response({'Data': None, 'message': message}, status=status.HTTP_200_OK)
