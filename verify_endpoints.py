import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_app.settings')
django.setup()

import json
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from quizzes.models import Quiz, Category
from attempts.models import Attempt

def test_endpoints():
    client = APIClient()
    # Use a unique username to avoid conflicts
    username = 'testviewer_unique_123'
    User.objects.filter(username=username).delete()
    user = User.objects.create_user(username=username, password='password', email='viewer@example.com')
    client.force_authenticate(user=user)
    
    category = Category.objects.create(name="Science_Unique")
    quiz = Quiz.objects.create(title="Science Quiz", category=category, created_by=user, status=Quiz.Status.PUBLISHED)
    
    # Test /api/v1/users/me/quizzes/
    url = reverse('me-quizzes')
    response = client.get(url)
    print(f"Me Quizzes Status: {response.status_code}")
    assert response.status_code == 200
    assert len(response.data) >= 1
    
    # Test /api/v1/users/me/attempts/
    Attempt.objects.create(user=user, quiz=quiz, attempt_number=1)
    url = reverse('me-attempts')
    response = client.get(url)
    print(f"Me Attempts Status: {response.status_code}")
    assert response.status_code == 200
    assert len(response.data) >= 1
    
    # Test /api/v1/analytics/quizzes/{id}/stats/
    url = reverse('quiz-stats', args=[quiz.id])
    response = client.get(url)
    print(f"Quiz Stats Status: {response.status_code}")
    assert response.status_code == 200
    assert 'total_attempts' in response.data
    
    # Test /api/v1/analytics/quizzes/{id}/leaderboard/
    url = reverse('leaderboard', args=[quiz.id])
    response = client.get(url)
    print(f"Leaderboard Status: {response.status_code}")
    assert response.status_code == 200
    
    print("All endpoints verified successfully!")

if __name__ == "__main__":
    try:
        test_endpoints()
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        User.objects.filter(username='testviewer_unique_123').delete()
        Category.objects.filter(name="Science_Unique").delete()
