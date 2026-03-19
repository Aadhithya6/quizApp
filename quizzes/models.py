import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    icon_url = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Easy'
        MEDIUM = 'MEDIUM', 'Medium'
        HARD = 'HARD', 'Hard'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='quizzes',
        db_index=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_quizzes',
        db_index=True
    )
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )
    is_public = models.BooleanField(default=True)
    passing_score = models.FloatField(null=True, blank=True)
    time_limit = models.IntegerField(null=True, blank=True)
    shuffle_questions = models.BooleanField(default=False)
    shuffle_options = models.BooleanField(default=False)
    allow_skip = models.BooleanField(default=False)
    max_attempts = models.IntegerField(null=True, blank=True)
    ai_prompt = models.TextField(null=True, blank=True)
    ai_model_used = models.CharField(max_length=100, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through='QuizTag', related_name='quizzes')

    class Meta:
        db_table = 'quizzes'
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return self.title

class QuizTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'quiz_tags'
        unique_together = ('quiz', 'tag')
