import uuid
from django.db import models
from django.conf import settings
from quizzes.models import Quiz
from questions.models import Question, Option

class Attempt(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        AUTO_SUBMITTED = 'AUTO_SUBMITTED', 'Auto Submitted'
        ABANDONED = 'ABANDONED', 'Abandoned'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='attempts',
        db_index=True
    )
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='attempts',
        db_index=True
    )
    attempt_number = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )
    score = models.FloatField(null=True, blank=True)
    is_passed = models.BooleanField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(null=True, blank=True) # in seconds
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        db_table = 'attempts'
        unique_together = ('user', 'quiz', 'attempt_number')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - Attempt {self.attempt_number}"

class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(
        Attempt, 
        on_delete=models.CASCADE, 
        related_name='answers',
        db_index=True
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE
    )
    selected_option = models.ForeignKey(
        Option, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    is_skipped = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'answers'
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"Answer for {self.question.id} in Attempt {self.attempt.id}"
