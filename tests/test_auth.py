from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from accounts.models import User

class AuthTests(BaseAPITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_and_token_generation(self):
        response = self.login(self.username, self.password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_verify_access_to_protected_endpoint(self):
        # Without login
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # With login
        self.login(self.username, self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)
