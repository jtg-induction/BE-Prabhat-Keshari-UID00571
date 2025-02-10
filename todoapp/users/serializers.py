from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

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
        