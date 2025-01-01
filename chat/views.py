from django.shortcuts import render, redirect
from sphereEngine.service import SphereEngineAPI
import requests
from django.http import JsonResponse

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