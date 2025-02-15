from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'password', 'date_joined', 'token'
        ]

    def get_token(self, instance):
        token = Token.objects.create(user=instance)
        return token.key

    def validate(self, validated_data):
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError(
                {'Password and confirm password do not match'}, code=status.HTTP_400_BAD_REQUEST
            )

        validated_data['password'] = make_password(validated_data['password'])

        return validated_data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                {"error": "Invalid email or password."},
                code=status.HTTP_400_BAD_REQUEST
            )

        validated_data['user'] = user
        return validated_data
