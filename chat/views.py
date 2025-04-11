from django.shortcuts import render, redirect
from sphereEngine.service import SphereEngineAPI
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import JsonResponse
from .models import CachedQuestion
from rest_framework.views import APIView
from .tasks import pre_generate_questions

from .generator import generate_high_quality_question

def chatPage(request, *args, **kwargs):
    api = SphereEngineAPI()
    compilers = api.get_compilers()
    compiler_list = compilers.get('items',[])
    # print(compilers)
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    return render(request, "chat/chatPage.html", {'compilers': compiler_list})

def fetch_submission_output(submission_id):
    url = f"https://203deddf.compilers.sphere-engine.com/api/v4/submissions/{submission_id}/output?access_token=409e09b9909c4e230776c63c69e09469"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text  # Return the output content
    else:
        return None  # Return None in case of failure

def submissionOutput(request, submission_id):
    output = fetch_submission_output(submission_id)
    
    if output:
        return JsonResponse({'output': output})
    else:
        return JsonResponse({'error': 'Unable to fetch output'}, status=400)
    
@api_view(['GET'])
def generate_question_api(request):
    difficulty = request.data.get("difficulty", "Easy").capitalize()
    if difficulty not in ["Easy", "Medium", "Hard"]:
        return Response({"error": "Invalid difficulty"}, status=status.HTTP_400_BAD_REQUEST)

    question = generate_high_quality_question(difficulty)
    return Response({"question": question})

class RandomQuestionAPIView(APIView):
    def get(self, request):
        difficulty = request.query_params.get('difficulty', 'easy')

        cached = CachedQuestion.objects.filter(difficulty=difficulty)
        if cached.exists():
            # Select a random question from the cache
            question = cached.order_by('?').first()
            
            # Get the part of the question before the first full stop
            question_text = question.question.strip().split('.')[0]  # Split at the first full stop
            
            return Response({
                'difficulty': question.difficulty,
                'question': question_text,  # Only the part before the first full stop
                'answer': question.answer.strip() if question.answer else 'No answer available'
            })

        # If no cached questions, generate and cache 100
        for _ in range(100):
            question_text = generate_high_quality_question(difficulty)
            CachedQuestion.objects.create(
                difficulty=difficulty,
                question=question_text.strip(),  # Ensure clean question text
                answer=""  # You can populate this with model answers if available
            )

        # Return one of the newly created questions
        first = CachedQuestion.objects.filter(difficulty=difficulty).order_by('?').first()
        return Response({
            'question': first.question.strip(),  # Strip extra spaces
            'answer': first.answer.strip() if first.answer else 'No answer available'
        })
