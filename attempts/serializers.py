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

class AttemptSummarySerializer(serializers.ModelSerializer):
    quiz_title = serializers.ReadOnlyField(source='quiz.title')
    total_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    wrong_answers = serializers.SerializerMethodField()

    class Meta:
        model = Attempt
        fields = (
            'id', 'quiz', 'quiz_title', 'score', 'is_passed',
            'total_questions', 'correct_answers', 'wrong_answers',
            'time_taken', 'status'
        )

    def get_total_questions(self, obj):
        return obj.quiz.questions.count()

    def get_correct_answers(self, obj):
        return obj.answers.filter(selected_option__is_correct=True).count()

    def get_wrong_answers(self, obj):
        # Questions that were answered but incorrectly (not skipped)
        return obj.answers.filter(selected_option__is_correct=False, is_skipped=False).count()
