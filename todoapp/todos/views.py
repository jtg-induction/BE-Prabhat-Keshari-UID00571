from rest_framework.viewsets import ModelViewSet

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
    def get_serializer_class(self):
        if self.action == 'create':
            return TodoViewSetCreateSerializer
 
        return TodoViewSetSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            return Todo.objects.filter(user__id=user_id)  
        return Todo.objects.all()