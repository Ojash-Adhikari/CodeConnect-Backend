from celery import shared_task
from .generator import generate_question  

@shared_task
def pre_generate_questions(difficulty="easy", count=100):
    from .models import CachedQuestion
    for _ in range(count):
        question = generate_question(difficulty)
        CachedQuestion.objects.create(
            difficulty=difficulty,
            question=question["question"],
            answer=question["answer"]
        )
