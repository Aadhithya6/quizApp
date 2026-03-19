from django.utils import timezone
from django.db import transaction
from .models import Attempt, Answer
from .scoring_service import calculate_attempt_score
from questions.models import Question

def start_quiz_attempt(user, quiz):
    """
    Starts a new quiz attempt for a user.
    Increments the attempt_number.
    """
    last_attempt = Attempt.objects.filter(user=user, quiz=quiz).order_by('-attempt_number').first()
    attempt_number = (last_attempt.attempt_number + 1) if last_attempt else 1

    # Check max_attempts
    if quiz.max_attempts and attempt_number > quiz.max_attempts:
        raise ValueError("Maximum attempts reached for this quiz.")

    attempt = Attempt.objects.create(
        user=user,
        quiz=quiz,
        attempt_number=attempt_number,
        status=Attempt.Status.IN_PROGRESS
    )
    return attempt

@transaction.atomic
def submit_quiz_answer(attempt, question_id, selected_option_id=None, is_skipped=False):
    """
    Submits or updates an answer for a question in an attempt.
    Idempotent.
    """
    if attempt.status != Attempt.Status.IN_PROGRESS:
        raise ValueError("Cannot submit answers for a completed attempt.")

    # Validate that the question belongs to the quiz
    question = Question.objects.get(id=question_id, quiz=attempt.quiz)

    answer, created = Answer.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={
            'selected_option_id': selected_option_id,
            'is_skipped': is_skipped,
            'answered_at': timezone.now()
        }
    )
    return answer

def finish_quiz_attempt(attempt):
    """
    Finishes a quiz attempt, calculates score, and sets final status.
    """
    if attempt.status != Attempt.Status.IN_PROGRESS:
        return attempt

    attempt.status = Attempt.Status.COMPLETED
    attempt.completed_at = timezone.now()
    
    # Calculate time taken
    duration = attempt.completed_at - attempt.started_at
    attempt.time_taken = int(duration.total_seconds())

    # Calculate score
    attempt = calculate_attempt_score(attempt)
    attempt.save()
    
    return attempt
