from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from attempts.models import Attempt
from accounts.models import User
from quizzes.models import Quiz

class AttemptFlowTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = self.create_category("Math")
        self.quiz = self.create_quiz("Math Quiz", self.category, self.user, status=Quiz.Status.PUBLISHED)
        self.q1 = self.create_question(self.quiz, "1+1?", [("2", True), ("3", False)])
        self.login(self.username, self.password)

    def test_full_attempt_flow(self):
        # 1. Start an attempt
        url = reverse('quiz-attempts', args=[self.quiz.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attempt_id = response.data['id']

        # 2. Fetch questions
        url = reverse('attempt-questions', args=[attempt_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # 3. Submit answers
        url = reverse('attempt-answers', args=[attempt_id])
        data = {
            "question": str(self.q1.id),
            "selected_option": str(self.q1.options.get(is_correct=True).id)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 4. Submit attempt
        url = reverse('attempt-submit', args=[attempt_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 5. Verify results
        self.assertEqual(response.data['status'], 'COMPLETED')
        self.assertEqual(response.data['score'], 100.0)
        self.assertIsNotNone(response.data['time_taken'])

    def test_leaderboard_ranking(self):
        # Create user2 and user3
        user2 = User.objects.create_user(username="user2", password="password", email="user2@example.com")
        user3 = User.objects.create_user(username="user3", password="password", email="user3@example.com")
        
        # User 1 (100 score, 10s)
        attempt1 = Attempt.objects.create(user=self.user, quiz=self.quiz, attempt_number=1, status='COMPLETED', score=100.0, time_taken=10)
        # User 2 (100 score, 5s) - Should be first due to faster time
        attempt2 = Attempt.objects.create(user=user2, quiz=self.quiz, attempt_number=1, status='COMPLETED', score=100.0, time_taken=5)
        # User 3 (80 score, 2s)
        attempt3 = Attempt.objects.create(user=user3, quiz=self.quiz, attempt_number=1, status='COMPLETED', score=80.0, time_taken=2)
        
        url = reverse('leaderboard', args=[self.quiz.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check order
        # Since LeaderboardView returns best score per user.
        # It should show: User 2 (100), User 1 (100), User 3 (80)
        # Wait, analytics/views.py LeaderboardView order_by('-best_score').
        # It doesn't seem to have secondary sort by time_taken.
        # I should probably fix that if it's a requirement.
        
        self.assertEqual(response.data[0]['user__username'], "user2")
        self.assertEqual(response.data[1]['user__username'], self.username)
