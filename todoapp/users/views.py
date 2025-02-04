import json

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions

from users.serializers import UserRegistrationSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """
        success response format
         {
           first_name: "",
           last_name: "",
           email: "",
           date_joined: "",
           "token"
         }
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
        

class UserLoginAPIView(APIView):
    """
        success response format
         {
           auth_token: ""
         }
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        