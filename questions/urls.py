from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, OptionViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet)
router.register('options', OptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
