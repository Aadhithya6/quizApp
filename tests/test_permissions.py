from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from quizzes.models import Quiz

class PermissionTests(BaseAPITestCase):
    def test_normal_user_cannot_publish_quiz(self):
        print("\n--- Running TEST: Normal User Cannot Publish Quiz ---")
        self.category = self.create_category("Science")
        quiz = self.create_quiz("User Quiz", self.category, self.user)
        
        self.login(self.username, self.password)
        print("Attempting to publish quiz as a normal user...")
        url = reverse('quiz-publish', args=[quiz.id])
        response = self.client.post(url)
        # Should be 403 Forbidden because normal user cannot publish
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("SUCCESS: Normal user access denied for publishing.")

    def test_unauthenticated_user_cannot_access_protected_endpoints(self):
        print("\n--- Running TEST: Unauthenticated User Cannot Access Protected Endpoints ---")
        url = reverse('quiz-list')
        # Listing is public, but creation is not
        print("Attempting to create a quiz while unauthenticated...")
        response = self.client.post(url, {"title": "No Auth Quiz"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("SUCCESS: Unauthenticated user access denied for creation.")

    def test_only_admin_can_create_categories(self):
        print("\n--- Running TEST: Only Admin Can Create Categories ---")
        url = reverse('category-list')
        self.login(self.username, self.password)
        print("Attempting to create a category as a normal user...")
        response = self.client.post(url, {"name": "User Category"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        print("Attempting to create a category as an administrator...")
        self.login("adminuser", "adminpassword123")
        response = self.client.post(url, {"name": "Admin Category"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("SUCCESS: Category creation restricted to administrators.")
