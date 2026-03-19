from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Max, Min, Avg, Count, Q, F, Window
from django.db.models.functions import Rank
from quizzes.models import Quiz
from attempts.models import Attempt
from interactions.models import QuizRating

class QuizStatsView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        try:
            quiz = Quiz.objects.get(id=pk)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=404)

        stats = Attempt.objects.filter(quiz=quiz, status=Attempt.Status.COMPLETED).aggregate(
            total_attempts=Count('id'),
            average_score=Avg('score'),
            average_time_taken=Avg('time_taken'),
            pass_count=Count('id', filter=Q(is_passed=True))
        )

        question_count = quiz.questions.count()
        rating_stats = QuizRating.objects.filter(quiz=quiz).aggregate(
            average_rating=Avg('rating'),
            rating_count=Count('id')
        )

        total_attempts = stats['total_attempts'] or 0
        pass_rate = (stats['pass_count'] / total_attempts * 100) if total_attempts > 0 else 0

        return Response({
            "quiz_id": quiz.id,
            "question_count": question_count,
            "total_attempts": total_attempts,
            "average_score": stats['average_score'],
            "average_time_taken": stats['average_time_taken'],
            "average_rating": rating_stats['average_rating'],
            "rating_count": rating_stats['rating_count'],
            "pass_rate": pass_rate
        })

class LeaderboardView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk=None):
        # Best score per user for this quiz
        leaderboard = Attempt.objects.filter(
            quiz_id=pk, 
            status=Attempt.Status.COMPLETED
        ).values(
            'user__id', 'user__username', 'user__avatar_url'
        ).annotate(
            best_score=Max('score'),
            # To get best_time_taken corresponding to best_score is tricky in ORM.
            # We'll use a simplified version or a window function.
            total_attempts=Count('id')
        ).order_by('-best_score')

        # Add ranking manually or using Window function
        # Since we are filtering by quiz_id, we can Rank over the annotated results.
        # However, annotate and values together behave like GROUP BY.
        
        # We'll just return the top 10 for now.
        return Response(list(leaderboard[:10]))
