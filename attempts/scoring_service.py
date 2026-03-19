from django.utils import timezone
from .models import Attempt, Answer
from questions.models import Question, Option

def calculate_attempt_score(attempt: Attempt):
    """
    Calculates the score for a quiz attempt.
    - SINGLE: Exact match.
    - MULTIPLE: All correct options must match.
    - TRUE_FALSE: Exact match.
    """
    category_scores = {} # For detailed breakdown if needed
    total_points = 0
    earned_points = 0

    # Get all questions in the quiz
    questions = Question.objects.filter(quiz=attempt.quiz).prefetch_related('options')
    
    # Get all answers for this attempt
    answers = Answer.objects.filter(attempt=attempt).select_related('question', 'selected_option')
    answer_map = {ans.question_id: ans for ans in answers}

    for question in questions:
        total_points += question.points
        answer = answer_map.get(question.id)

        if not answer or answer.is_skipped or not answer.selected_option:
            continue

        # Check if the answer is correct
        if question.question_type in [Question.QuestionType.SINGLE, Question.QuestionType.TRUE_FALSE]:
            if answer.selected_option.is_correct:
                earned_points += question.points
        elif question.question_type == Question.QuestionType.MULTIPLE:
            # For MULTIPLE CHOICE, we need to handle it differently if multiple options can be selected.
            # However, the Answer model currently only stores one selected_option.
            # The specification says: "MULTIPLE -> all correct options must match"
            # This implies the user can select multiple options, but the schema only allows one.
            # WAIT: "selected_option_id (UUID, FK -> Option.id, nullable) <- NULL means skipped"
            # This suggests a single selection even for MULTIPLE choice? 
            # Or should I have a ManyToMany for MULTIPLE?
            # Looking at the requirement: "MULTIPLE -> all correct options must match"
            # If the user can only select one option in the Answer model, then MULTIPLE is impossible with that schema.
            # I will stick to the schema as requested, but maybe there's a misunderstanding.
            # "selected_option_id (UUID, FK -> Option.id, nullable)" is a singular field.
            # If I need multiple answers per question, I'd need multiple Answer rows or a junction table.
            # The schema says: "Answer -> UNIQUE (attempt_id, question_id)"
            # This confirms ONE Answer per question.
            # If so, MULTIPLE must mean something else or the schema is limiting.
            # I'll assume for now that only one option can be selected as per the schema.
            if answer.selected_option.is_correct:
                # Check if there are other correct options that were NOT selected.
                # If there are, then the answer is NOT fully correct.
                correct_options_count = Option.objects.filter(question=question, is_correct=True).count()
                if correct_options_count == 1:
                    earned_points += question.points
                else:
                    # Partial credit or no credit? Spec says "all correct options must match".
                    # If only one was selected and multiple were correct, then not all matched.
                    pass 
        
    score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0
    attempt.score = score_percentage
    attempt.is_passed = (score_percentage >= attempt.quiz.passing_score) if attempt.quiz.passing_score is not None else True
    return attempt
