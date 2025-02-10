from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

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
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'date_joined']

    def create(self, validated_data):
        user = CustomUser(
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, instance):
        represntation = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        represntation['token'] = token.key
        return represntation
    