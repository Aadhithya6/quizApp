import os
from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Category, Tag, Quiz
from .serializers import CategorySerializer, TagSerializer, QuizSerializer, QuizCreateUpdateSerializer
from .services import submit_quiz_for_review, publish_quiz, reject_quiz
from common.permissions import IsAdminUser, IsOwnerOrReadOnly
from interactions.models import QuizRating, Notification
from interactions.serializers import QuizRatingSerializer
from attempts.models import Attempt
from attempts.serializers import AttemptSerializer
from attempts.services import start_quiz_attempt

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('category', 'difficulty', 'status', 'tags')
    search_fields = ('title', 'topic', 'description')
    ordering_fields = ('created_at', 'published_at')

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.role == 'ADMIN' or self.action == 'pending'):
            return Quiz.objects.all()
        # For public listing, only show published quizzes
        return Quiz.objects.filter(status=Quiz.Status.PUBLISHED, is_active=True)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuizCreateUpdateSerializer
        return QuizSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        if self.action in ['publish', 'reject']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        generate_with_ai = serializer.validated_data.pop('generate_with_ai', False)
        num_questions = serializer.validated_data.pop('num_questions', 5)
        
        quiz = serializer.save(created_by=self.request.user)
        
        if generate_with_ai:
            from .services.ai_service import generate_quiz
            from .services.quiz_generator_service import create_questions_from_ai
            
            try:
                # 1. Call AI Service
                questions_data = generate_quiz(
                    topic=quiz.topic or quiz.title,
                    difficulty=quiz.difficulty,
                    num_questions=num_questions
                )
                
                # 2. Parse & Save Questions
                if questions_data:
                    create_questions_from_ai(quiz, questions_data)
                    
                    # 3. Update AI-related fields
                    quiz.ai_prompt = f"Topic: {quiz.topic or quiz.title}, Difficulty: {quiz.difficulty}"
                    quiz.ai_model_used = os.getenv('NVIDIA_MODEL', 'meta/llama-3.1-405b-instruct')
                    quiz.save()
                    
            except Exception as e:
                # If AI fails, keep status as DRAFT and set an error field if needed
                # (Assuming DRAFT is default status)
                quiz.status = Quiz.Status.DRAFT
                quiz.save()
                # We could also add a notification for the user here
                print(f"AI Generation failed for Quiz {quiz.id}: {str(e)}")

    @decorators.action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        quiz = submit_quiz_for_review(quiz)
        return Response(QuizSerializer(quiz).data)

    @decorators.action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        quiz = self.get_object()
        quiz = publish_quiz(quiz)
        return Response(QuizSerializer(quiz).data)

    @decorators.action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        quiz = self.get_object()
        quiz = reject_quiz(quiz)
        return Response(QuizSerializer(quiz).data)

    @decorators.action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending(self, request):
        """Admin review queue: shows all quizzes in PENDING status."""
        quizzes = Quiz.objects.filter(status=Quiz.Status.PENDING)
        page = self.paginate_queryset(quizzes)
        if page is not None:
            serializer = QuizSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def attempts(self, request, pk=None):
        """Starts a new attempt for the quiz (Nested resource style)."""
        quiz = self.get_object()
        if quiz.status != Quiz.Status.PUBLISHED:
            return Response({"detail": "Quiz is not published."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            attempt = start_quiz_attempt(request.user, quiz)
            return Response(AttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=['post'], url_path='retry', permission_classes=[permissions.IsAuthenticated])
    def retry(self, request, pk=None):
        """Creates a new attempt (shorthand for start attempt)."""
        return self.attempts(request, pk)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rating(self, request, pk=None):
        """Allows a user to rate a quiz."""
        quiz = self.get_object()
        serializer = QuizRatingSerializer(data=request.data)
        if serializer.is_valid():
            # Check if user already rated
            rating, created = QuizRating.objects.update_or_create(
                user=request.user,
                quiz=quiz,
                defaults={'rating': serializer.validated_data['rating'], 'review': serializer.validated_data.get('review', '')}
            )
            return Response(QuizRatingSerializer(rating).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def ratings(self, request, pk=None):
        """Returns all ratings for a quiz."""
        quiz = self.get_object()
        ratings = quiz.ratings.all()
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = QuizRatingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = QuizRatingSerializer(ratings, many=True)
        return Response(serializer.data)
