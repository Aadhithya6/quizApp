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
        print("\n--- Running TEST: Create Quiz (AI Assisted) ---")
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
        print("SUCCESS: Quiz created with AI generated questions.")

    def test_submit_quiz_for_review(self):
        print("\n--- Running TEST: Submit Quiz for Review ---")
        quiz = self.create_quiz("New Quiz", self.category, self.user)
        # Ensure initial status
        self.assertEqual(quiz.status, Quiz.Status.DRAFT) 
        
        url = reverse('quiz-submit', args=[quiz.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quiz.refresh_from_db()
        self.assertEqual(quiz.status, Quiz.Status.PENDING)
        print("SUCCESS: Quiz submitted for admin review.")

    def test_admin_publishes_quiz(self):
        print("\n--- Running TEST: Admin Publishes Quiz ---")
        quiz = self.create_quiz("Pending Quiz", self.category, self.user)
        quiz.status = Quiz.Status.PENDING
        quiz.save()
        
        # Login as Admin
        print("Logging in as administrator...")
        self.login("adminuser", "adminpassword123")
        url = reverse('quiz-publish', args=[quiz.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quiz.refresh_from_db()
        self.assertEqual(quiz.status, Quiz.Status.PUBLISHED)
        print("SUCCESS: Quiz published by administrator.")

    def test_quiz_visibility_in_public_listing(self):
        print("\n--- Running TEST: Quiz Visibility in Public Listing ---")
        # Create a draft and a published quiz
        self.create_quiz("Draft Quiz", self.category, self.user, status=Quiz.Status.DRAFT)
        self.create_quiz("Published Quiz", self.category, self.user, status=Quiz.Status.PUBLISHED)
        
        # Better be explicit
        Quiz.objects.filter(title="Draft Quiz").update(status=Quiz.Status.DRAFT)
        Quiz.objects.filter(title="Published Quiz").update(status=Quiz.Status.PUBLISHED)
        
        url = reverse('quiz-list')
        print("Attempting to list quizzes while unauthenticated...")
        # Should only see published quizzes if unauthenticated or requester is not owner/admin
        self.client.credentials() # Logout
        from django.core.cache import cache
        cache.clear()
        response = self.client.get(url)
        print(f"DEBUG: Quizzes found: {[q['title'] for q in response.data['results']]}")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Published Quiz")
        print("SUCCESS: Only published quizzes are visible to public.")
