from rest_framework import serializers
from .models import Attempt, Answer
from questions.serializers import QuestionPublicSerializer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'selected_option', 'is_skipped', 'answered_at')

class AttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.ReadOnlyField(source='quiz.title')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Attempt
        fields = (
            'id', 'user', 'user_username', 'quiz', 'quiz_title', 'attempt_number',
            'status', 'score', 'is_passed', 'started_at', 'completed_at',
            'time_taken', 'is_reviewed'
        )
        read_only_fields = ('id', 'user', 'attempt_number', 'status', 'score', 'is_passed', 'started_at', 'completed_at', 'time_taken')

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'selected_option', 'is_skipped')
