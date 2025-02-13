from rest_framework import viewsets

from projects.models import Project
from projects.serializers import (
    ProjectUpdateMemberSerializer, ProjectViewSerializer
)


class ProjectMemberApiViewSet(viewsets.ModelViewSet):
    """
       constraints
        - a user can be a member of max 2 projects only
        - a project can have at max N members defined in database for each project
       functionalities
       - add users to projects

         Request
         { user_ids: [1,2,...n] }
         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }
         following are the possible status messages
         case1: if user is added successfully then - "Member added Successfully"
         case2: if user is already a member then - "User is already a Member"
         case3: if user is already added to 2 projects - "Cannot add as User is a member in two projects"

         there will be many other cases think of that

       - update to remove users from projects

         Request
         { user_ids: [1,2,...n] }

         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }

         there will be many other cases think of that and share on forum
    """
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if 'add' in self.request.path or 'remove' in self.request.path:
            return ProjectUpdateMemberSerializer
        else:
            return ProjectViewSerializer
