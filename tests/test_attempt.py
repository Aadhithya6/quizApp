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
        print("\n--- Running TEST: Full Attempt Flow ---")
        # 1. Start an attempt
        print("Starting a new attempt...")
        url = reverse('quiz-attempts', args=[self.quiz.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attempt_id = response.data['id']
        print(f"Attempt started. ID: {attempt_id}")
        
        # 2. Fetch questions
        print("Fetching questions for the attempt...")
        url = reverse('attempt-questions', args=[attempt_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print("Questions fetched successfully.")
        
        # 3. Submit answers
        print("Submitting an answer...")
        url = reverse('attempt-answers', args=[attempt_id])
        data = {
            "question": str(self.q1.id),
            "selected_option": str(self.q1.options.get(is_correct=True).id)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Answer submitted successfully.")
        
        # 4. Submit attempt
        print("Finishing and submitting the attempt...")
        url = reverse('attempt-submit', args=[attempt_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Attempt submitted.")
        
        # 5. Verify results
        print("Verifying attempt results...")
        self.assertEqual(response.data['status'], 'COMPLETED')
        self.assertEqual(response.data['score'], 100.0)
        self.assertIsNotNone(response.data['time_taken'])
        print(f"SUCCESS: Attempt flow completed. Score: {response.data['score']}%")

    def test_leaderboard_ranking(self):
        print("\n--- Running TEST: Leaderboard Ranking ---")
        # Create user2 and user3
        print("Creating additional users and attempts for testing ranking...")
        user2 = User.objects.create_user(username="user2", password="password", email="user2@example.com")
        user3 = User.objects.create_user(username="user3", password="password", email="user3@example.com")
        
        # User 1 (100 score, 10s)
        Attempt.objects.create(user=self.user, quiz=self.quiz, attempt_number=1, status='COMPLETED', score=100.0, time_taken=10)
        # User 2 (100 score, 5s) - Should be first due to faster time
        Attempt.objects.create(user=user2, quiz=self.quiz, attempt_number=1, status='COMPLETED', score=100.0, time_taken=5)
        # User 3 (80 score, 2s)
        Attempt.objects.create(user=user3, quiz=self.quiz, attempt_number=1, status='COMPLETED', score=80.0, time_taken=2)
        
        print("Fetching leaderboard data...")
        url = reverse('leaderboard', args=[self.quiz.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check order
        print("Verifying user rankings based on score and time...")
        self.assertEqual(response.data[0]['user__username'], "user2")
        self.assertEqual(response.data[1]['user__username'], self.username)
        print(f"SUCCESS: Leaderboard order verified: {response.data[0]['user__username']}, {response.data[1]['user__username']}")
