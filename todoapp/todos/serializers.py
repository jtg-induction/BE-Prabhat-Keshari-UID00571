from django.contrib.auth import get_user_model
from rest_framework import serializers

from todos.models import Todo
from users.serializers import UserSerializer


class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format='%I:%M %p, %d %b, %Y'
    )

    class Meta:
        model = Todo
        fields = ['id', 'name', 'status', 'created_at', 'creator']

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"
    
    def get_creator(self, obj):
        creator_data = UserSerializer(obj.user).data  
        creator_data.pop('id', None)
        return creator_data


class TodoDateRangeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format='%I:%M %p, %d %b, %Y'
    )

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Todo
        fields = ['id', 'name', 'creator', 'email', 'created_at', 'status']


class TodoViewSetCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user",
                                                 queryset=get_user_model().objects.all())
    todo = serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['user_id', 'todo']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            "name": representation["todo"],
            "done": instance.done,
            "date_created": instance.date_created.isoformat()
        }


class TodoViewSetSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo = serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done']