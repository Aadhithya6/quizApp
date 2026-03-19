from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TagViewSet, QuizViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('quizzes', QuizViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
