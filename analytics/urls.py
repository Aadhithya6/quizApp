from django.urls import path
from .views import QuizStatsView, LeaderboardView

urlpatterns = [
    path('quizzes/<uuid:pk>/stats/', QuizStatsView.as_view({'get': 'retrieve'}), name='quiz-stats'),
    path('quizzes/<uuid:pk>/leaderboard/', LeaderboardView.as_view({'get': 'retrieve'}), name='leaderboard'),
]
