import uuid
from django.db import models
from quizzes.models import Quiz

class Question(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Easy'
        MEDIUM = 'MEDIUM', 'Medium'
        HARD = 'HARD', 'Hard'

    class QuestionType(models.TextChoices):
        SINGLE = 'SINGLE', 'Single Choice'
        MULTIPLE = 'MULTIPLE', 'Multiple Choice'
        TRUE_FALSE = 'TRUE_FALSE', 'True/False'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='questions',
        db_index=True
    )
    text = models.TextField()
    explanation = models.TextField(null=True, blank=True)
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM
    )
    question_type = models.CharField(
        max_length=15,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE
    )
    order_index = models.IntegerField(default=0)
    points = models.IntegerField(default=1)
    image_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions'
        ordering = ['order_index']

    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='options',
        db_index=True
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order_index = models.IntegerField(default=0)
    image_url = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'options'
        ordering = ['order_index']

    def __str__(self):
        return self.text[:50]
