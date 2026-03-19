import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from quizzes.models import Quiz

class QuizRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='ratings',
        db_index=True
    )
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_ratings'
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user.username} rated {self.quiz.title}: {self.rating}"

class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='following',
        db_index=True
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='followers',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        unique_together = ('follower', 'following')
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(follower=models.F('following')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        QUIZ = 'QUIZ', 'Quiz'
        RESULT = 'RESULT', 'Result'
        LEADERBOARD = 'LEADERBOARD', 'Leaderboard'
        FOLLOW = 'FOLLOW', 'Follow'
        RATING = 'RATING', 'Rating'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        db_index=True
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=NotificationType.choices
    )
    reference_id = models.UUIDField(null=True, blank=True)
    reference_type = models.CharField(max_length=50, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
