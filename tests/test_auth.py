from django.urls import reverse
from rest_framework import status
from .base import BaseAPITestCase
from accounts.models import User

class AuthTests(BaseAPITestCase):
    def test_user_registration(self):
        print("\n--- Running TEST: User Registration ---")
        url = reverse('register')
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        print("SUCCESS: User registration completed.")

    def test_login_and_token_generation(self):
        print("\n--- Running TEST: Login and Token Generation ---")
        response = self.login(self.username, self.password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        print("SUCCESS: Login successful and tokens generated.")

    def test_verify_access_to_protected_endpoint(self):
        print("\n--- Running TEST: Verify Access to Protected Endpoint ---")
        # Without login
        print("Checking unauthorized access...")
        url = reverse('me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # With login
        print("Checking authorized access after login...")
        self.login(self.username, self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)
        print("SUCCESS: Protected endpoint access verified.")
