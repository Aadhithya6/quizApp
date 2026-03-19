from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Category, Quiz

class QuizAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        # Create a test category
        self.category = Category.objects.create(
            name='General Knowledge',
            description='Test category'
        )
        # Create a test quiz
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            category=self.category,
            created_by=self.user,
            status=Quiz.Status.PUBLISHED,
            is_active=True
        )
        self.client.force_authenticate(user=self.user)

    def test_get_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_quizzes(self):
        url = reverse('quiz-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_quiz(self):
        url = reverse('quiz-list')
        data = {
            'title': 'New Quiz',
            'category': self.category.id,
            'difficulty': 'MEDIUM',
            'status': 'DRAFT',
            'is_public': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)
