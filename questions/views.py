from rest_framework import viewsets, permissions
from .models import Question, Option
from .serializers import QuestionSerializer, OptionSerializer
from common.permissions import IsAdminOrModerator, IsOwnerOrReadOnly

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # The quiz creator or admin can manage questions
            return [IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]
