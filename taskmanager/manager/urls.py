from django.urls import path, include
from rest_framework import routers
from manager.views import TaskViewSet, TaskGroupViewSet

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"task_groups", TaskGroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
