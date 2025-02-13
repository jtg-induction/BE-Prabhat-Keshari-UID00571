from django.urls import path
from rest_framework import routers

from projects.views import ProjectMemberApiViewSet

app_name = 'projects'

router = routers.SimpleRouter()

router.register(r'projects', ProjectMemberApiViewSet, 'projects')

urlpatterns = [
    path('projects/add/<int:pk>/',
         ProjectMemberApiViewSet.as_view({'patch': 'partial_update'}), name='project-add'
         ),
    path('projects/remove/<int:pk>/',
         ProjectMemberApiViewSet.as_view({'patch': 'partial_update'}), name='project-remove'
         )
]

urlpatterns += router.urls
