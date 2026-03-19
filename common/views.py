from rest_framework import viewsets, permissions
from rest_framework.response import Response
from quizzes.models import Quiz
from quizzes.serializers import QuizSerializer
from rest_framework.filters import SearchFilter

class GlobalSearchView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response([])
        
        quizzes = Quiz.objects.filter(
            status=Quiz.Status.PUBLISHED
        ).filter(
            title__icontains=query
        ) | Quiz.objects.filter(
            status=Quiz.Status.PUBLISHED
        ).filter(
            topic__icontains=query
        )
        
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
