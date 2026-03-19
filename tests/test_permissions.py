from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from quizzes.models import Quiz

class PermissionTests(BaseAPITestCase):
    def test_normal_user_cannot_publish_quiz(self):
        self.category = self.create_category("Science")
        quiz = self.create_quiz("User Quiz", self.category, self.user)
        
        self.login(self.username, self.password)
        url = reverse('quiz-publish', args=[quiz.id])
        response = self.client.post(url)
        # Should be 403 Forbidden because normal user cannot publish
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access_protected_endpoints(self):
        url = reverse('quiz-list')
        # Listing is public, but creation is not
        response = self.client.post(url, {"title": "No Auth Quiz"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admin_can_create_categories(self):
        url = reverse('category-list')
        self.login(self.username, self.password)
        response = self.client.post(url, {"name": "User Category"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.login("adminuser", "adminpassword123")
        response = self.client.post(url, {"name": "Admin Category"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
