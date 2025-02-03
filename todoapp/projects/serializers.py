from rest_framework import serializers
from projects.models import Project
from users.models import CustomUser


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    existing_member_count = serializers.IntegerField()

    class Meta:
        model = Project
        fields = [
            "id", "name", "status", "existing_member_count", "max_members"
        ]

    def get_status(self, obj):
        if obj.status == 0:
            return "To be started"
        elif obj.status == 1:
            return "In progress"
        return "Completed"


class ProjectWithMemberName(serializers.ModelSerializer):
    done = serializers.SerializerMethodField()
    project_name = serializers.CharField(source="name")

    def get_done(self, obj):
        if obj.status == 0 or obj.status == 1:
            return False
        return True

    class Meta:
        model = Project
        fields = ['project_name', 'done', 'max_members']


class ProjectReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="name")
    report = serializers.SerializerMethodField()

    def get_report(self, obj):
        user_reports = []
        for user in obj.reports:
            user_report = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "pending_count": user.pending_count,
                "completed_count": user.completed_count
            }
            user_reports.append(user_report)
        return user_reports

    class Meta:
        model = Project
        fields = ['project_title', 'report']


class UserProjectSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.SerializerMethodField()
    in_progress_projects = serializers.SerializerMethodField()
    completed_projects = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "first_name", "last_name", "email", "to_do_projects", 
            "in_progress_projects", "completed_projects"
        )

    def get_to_do_projects(self, obj):
        return obj.to_do if obj.to_do else []

    def get_in_progress_projects(self, obj):
        return obj.in_progress if obj.in_progress else []

    def get_completed_projects(self, obj):
        return obj.completed if obj.completed else []
