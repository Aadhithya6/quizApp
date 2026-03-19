from django.utils import timezone
from ..models import Quiz

def submit_quiz_for_review(quiz: Quiz):
    """
    Submits a quiz for expert review before publishing.
    """
    if quiz.status == Quiz.Status.DRAFT:
        quiz.status = Quiz.Status.PENDING
        quiz.save()
    return quiz

def publish_quiz(quiz: Quiz):
    """
    Publishes a quiz, making it available for users to attempt.
    """
    if quiz.status == Quiz.Status.PENDING:
        quiz.status = Quiz.Status.PUBLISHED
        quiz.published_at = timezone.now()
        quiz.save()
    return quiz

def reject_quiz(quiz: Quiz):
    """
    Rejects a pending quiz, moving it back to draft status.
    """
    if quiz.status == Quiz.Status.PENDING:
        quiz.status = Quiz.Status.DRAFT
        quiz.save()
    return quiz
