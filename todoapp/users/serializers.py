from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']


class UserStatsSerializer(serializers.ModelSerializer):

    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'completed_count', 'pending_count'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name',
                  'last_name', 'password', 'date_joined', 'token']

    def get_token(self, instance):
        token = Token.objects.create(user=instance)
        return token.key

    def validate(self, validated_data):
        confirm_password = self.context['request'].data.get(
            'confirm_password', None
        )

        if not confirm_password:
            raise serializers.ValidationError(
                {"confirm_password: This field is required"}
            )

        if validated_data['password'] != confirm_password:
            raise serializers.ValidationError(
                {'Password and confirm password do not match'}
            )

        validated_data['password'] = make_password(validated_data['password'])

        return validated_data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, validated_data):
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                {"error": "Invalid email or password."},
                code=status.HTTP_400_BAD_REQUEST
            )

        validated_data['user'] = user
        return validated_data
