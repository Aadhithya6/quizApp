from django.db import transaction
from questions.models import Question, Option

@transaction.atomic
def create_questions_from_ai(quiz, ai_data: list):
    """
    Parses AI-generated JSON data and creates Question and Option objects in the database.
    Ensures correct option marking and maintains order indices.
    """
    created_questions = []
    
    for index, q_data in enumerate(ai_data):
        # Basic validation
        if not all(k in q_data for k in ('question', 'options', 'correct_answer', 'type')):
            continue
            
        # Create Question
        question = Question.objects.create(
            quiz=quiz,
            text=q_data['question'],
            explanation=q_data.get('explanation'),
            difficulty=quiz.difficulty,
            question_type=q_data['type'],
            order_index=index,
            points=1 # Default points
        )
        
        # Create Options
        correct_text = q_data['correct_answer']
        options_data = q_data['options']
        
        for opt_index, opt_text in enumerate(options_data):
            # The AI might return the label (A, B, C, D) or the text itself.
            # Usually better to check if correct_answer matches the text or the label.
            # For simplicity, we assume correct_answer is the text or a specific label if we prompted for it.
            # In our prompt, we asked for the text or value.
            
            is_correct = (opt_text == correct_text)
            
            Option.objects.create(
                question=question,
                text=opt_text,
                is_correct=is_correct,
                order_index=opt_index
            )
            
        created_questions.append(question)
        
    return created_questions
