from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from users.serializers import UserLoginSerializer, UserRegistrationSerializer


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
    permission_classes = []
    serializer_class = UserRegistrationSerializer


class UserLoginAPIView(APIView):
    """
        success response format
         {
           auth_token: ""
         }
    """

    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
