from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView

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


class UserLoginAPIView(GenericAPIView):
    """
        success response format
         {
           auth_token: ""
         }
    """

    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"Email or Password is not valid."}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"auth_token": token.key}, status=status.HTTP_200_OK)
