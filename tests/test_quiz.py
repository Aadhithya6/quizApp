from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from quizzes.models import Quiz
from unittest.mock import patch

class QuizLifecycleTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = self.create_category("Science")
        self.login(self.username, self.password)

    @patch('quizzes.services.ai_service.generate_quiz')
    def test_create_quiz(self, mock_ai):
        mock_ai.return_value = [{"question": "Q1", "options": ["A", "B", "C", "D"], "correct_answer": "A", "explanation": "E", "type": "SINGLE"}]
        url = reverse('quiz-list')
        data = {
            "title": "AI Science Quiz",
            "category": str(self.category.id),
            "difficulty": "MEDIUM",
            "topic": "Physics",
            "generate_with_ai": True,
            "num_questions": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.filter(title="AI Science Quiz").count(), 1)

    def test_submit_quiz_for_review(self):
        quiz = self.create_quiz("New Quiz", self.category, self.user)
        # Ensure initial status
        self.assertEqual(quiz.status, Quiz.Status.DRAFT) 
        
        url = reverse('quiz-submit', args=[quiz.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quiz.refresh_from_db()
        self.assertEqual(quiz.status, Quiz.Status.PENDING)

    def test_admin_publishes_quiz(self):
        quiz = self.create_quiz("Pending Quiz", self.category, self.user)
        quiz.status = Quiz.Status.PENDING
        quiz.save()
        
        # Login as Admin
        self.login("adminuser", "adminpassword123")
        url = reverse('quiz-publish', args=[quiz.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quiz.refresh_from_db()
        self.assertEqual(quiz.status, Quiz.Status.PUBLISHED)

    def test_quiz_visibility_in_public_listing(self):
        # Create a draft and a published quiz
        self.create_quiz("Draft Quiz", self.category, self.user, status=Quiz.Status.DRAFT)
        self.create_quiz("Published Quiz", self.category, self.user, status=Quiz.Status.PUBLISHED)
        
        # Better be explicit
        Quiz.objects.filter(title="Draft Quiz").update(status=Quiz.Status.DRAFT)
        Quiz.objects.filter(title="Published Quiz").update(status=Quiz.Status.PUBLISHED)
        
        url = reverse('quiz-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see published quizzes if unauthenticated or requester is not owner/admin
        self.client.credentials() # Logout
        from django.core.cache import cache
        cache.clear()
        response = self.client.get(url)
        print(f"\nDEBUG: Quizzes found: {[q['title'] for q in response.data['results']]}")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Published Quiz")
