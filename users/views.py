from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializers import CreateUserSerializer

from . import util


class TestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        qs = util.readFile(15)
        serialized = PatientSerializer(qs, many=True)
        return Response(serialized.data)

    def post(self, request, *args, **kwargs):
        # This post method just for simulate sumulation
        util.simulator()
        return Response({'Simulation': 'Finished '})


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
    print("Request data", request.data)
    serializer = CreateUserSerializer(data=request.data)
    response_data = {
        'error': None,
        'data': None
    }
    if serializer.is_valid():
        user = serializer.save()  # save to user db
        response_data['data'] = {'Success': user.id}
        response_status = status.HTTP_200_OK
    else:
        response_data['error'] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_status)
