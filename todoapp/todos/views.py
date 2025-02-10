from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from todos.models import Todo
from todos.serializers import TodoViewSetCreateSerializer, TodoViewSetSerializer


class TodoAPIViewSet(ModelViewSet):
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return TodoViewSetCreateSerializer
 
        return TodoViewSetSerializer
    
    def get_queryset(self): 
        token = self.request.auth.key
        user_id = Token.objects.get(key=token).user
        return Todo.objects.filter(user=user_id)
    
        
