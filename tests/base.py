from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from quizzes.models import Category, Quiz, Tag
from questions.models import Question, Option

from django.core.cache import cache

class BaseAPITestCase(APITestCase):
    def setUp(self):
        cache.clear()
        self.username = "testuser"
        self.password = "testpass123"
        self.email = "testuser@example.com"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
            role=User.Role.USER
        )
        
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            password="adminpassword123",
            email="admin@example.com"
        )
        self.admin_user.role = User.Role.ADMIN
        self.admin_user.save()

    def login(self, username, password):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': username,
            'password': password
        })
        if response.status_code == 200:
            token = response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return response

    def create_category(self, name="General Knowledge"):
        return Category.objects.create(name=name, slug=name.lower().replace(" ", "-"))

    def create_quiz(self, title="Sample Quiz", category=None, user=None, status=Quiz.Status.DRAFT):
        if not category:
            category = self.create_category()
        if not user:
            user = self.user
        return Quiz.objects.create(
            title=title,
            category=category,
            created_by=user,
            status=status
        )

    def create_question(self, quiz, text="What is 2+2?", options=None):
        question = Question.objects.create(
            quiz=quiz,
            text=text,
            question_type=Question.QuestionType.SINGLE
        )
        if options:
            for opt_text, is_correct in options:
                Option.objects.create(
                    question=question,
                    text=opt_text,
                    is_correct=is_correct
                )
        return question
