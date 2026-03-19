from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttemptViewSet

router = DefaultRouter()
router.register('attempts', AttemptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
