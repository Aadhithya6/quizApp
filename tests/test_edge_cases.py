from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from quizzes.models import Quiz
import uuid

class EdgeCaseTests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.login(self.username, self.password)

    def test_invalid_quiz_id_returns_404(self):
        invalid_id = uuid.uuid4()
        url = reverse('quiz-detail', args=[invalid_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_option_id_returns_error(self):
        category = self.create_category()
        quiz = self.create_quiz("Quiz", category, status=Quiz.Status.PUBLISHED)
        q1 = self.create_question(quiz, "Q?")
        
        # Start attempt
        start_url = reverse('quiz-attempts', args=[quiz.id])
        attempt_id = self.client.post(start_url).data['id']
        
        url = reverse('attempt-answers', args=[attempt_id])
        data = {
            "question": str(q1.id),
            "selected_option": str(uuid.uuid4()) # Invalid ID
        }
        response = self.client.post(url, data)
        # Serializer should catch invalid UUID or non-existent FK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submitting_duplicate_answers_updates(self):
        category = self.create_category()
        quiz = self.create_quiz("Quiz", category, status=Quiz.Status.PUBLISHED)
        q1 = self.create_question(quiz, "Q?", [("A", True), ("B", False)])
        
        start_url = reverse('quiz-attempts', args=[quiz.id])
        attempt_id = self.client.post(start_url).data['id']
        
        url = reverse('attempt-answers', args=[attempt_id])
        data1 = {"question": str(q1.id), "selected_option": str(q1.options.first().id)}
        self.client.post(url, data1)
        
        data2 = {"question": str(q1.id), "selected_option": str(q1.options.last().id)}
        response = self.client.post(url, data2)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['selected_option']), str(q1.options.last().id))
