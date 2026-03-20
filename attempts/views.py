from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from .models import Attempt, Answer
from .serializers import AttemptSerializer, AnswerSerializer, AnswerCreateSerializer
from .services import start_quiz_attempt, submit_quiz_answer, finish_quiz_attempt
from quizzes.models import Quiz
from questions.models import Question
from questions.serializers import QuestionPublicSerializer, QuestionSerializer
import random

class AttemptViewSet(viewsets.ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


    @decorators.action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        attempt = self.get_object()
        if attempt.status != Attempt.Status.IN_PROGRESS:
            return Response({"error": "Attempt is not in progress."}, status=status.HTTP_400_BAD_REQUEST)

        questions = Question.objects.filter(quiz=attempt.quiz).prefetch_related('options')
        
        # Apply shuffle logic if quiz settings allow
        questions_list = list(questions)
        if attempt.quiz.shuffle_questions:
            random.shuffle(questions_list)

        if attempt.quiz.shuffle_options:
            for q in questions_list:
                options = list(q.options.all())
                random.shuffle(options)
                q.shuffled_options = options # Virtual attribute for serializer if needed? 
                # Better to handle this in a custom serializer or just return data manually.

        serializer = QuestionPublicSerializer(questions_list, many=True)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=['post'])
    def answers(self, request, pk=None):
        attempt = self.get_object()
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            answer = submit_quiz_answer(
                attempt, 
                serializer.validated_data['question'].id,
                serializer.validated_data.get('selected_option').id if serializer.validated_data.get('selected_option') else None,
                serializer.validated_data.get('is_skipped', False)
            )
            return Response(AnswerSerializer(answer).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        attempt = finish_quiz_attempt(attempt)
        return Response(AttemptSerializer(attempt).data)

    @decorators.action(detail=True, methods=['get'])
    def review(self, request, pk=None):
        attempt = self.get_object()
        if attempt.status != Attempt.Status.COMPLETED:
            return Response({"error": "Attempt is not completed."}, status=status.HTTP_400_BAD_REQUEST)

        questions = Question.objects.filter(quiz=attempt.quiz).prefetch_related('options')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
