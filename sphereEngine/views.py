import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .service import SphereEngineAPI

class CompileCodeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            source_code = data.get('source_code')
            compiler_id = data.get('compilerId')
            version_id = data.get('versionId')

            if not source_code or not compiler_id or not version_id:
                return JsonResponse({'error': 'Source code, compiler ID, and version ID are required'}, status=400)

            api = SphereEngineAPI()
            result = api.compile_code(source_code, compiler_id,version_id)
            return JsonResponse(result)
        except Exception as e:
            print(f'Error in CompileCodeView: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)


class ListCompilersView(View):
    def get(self, request):
        api = SphereEngineAPI()
        auth_test = api.test_authentication()
        if 'message' in auth_test and auth_test['message'] != 'OK':
            return JsonResponse(auth_test, status=400)

        compilers = api.get_compilers()
        return JsonResponse(compilers)
    
class GetProblemsView(View):
    def get(self, request):
        api = SphereEngineAPI()
        result = api.get_problems()
        return JsonResponse(result)

class GetSubmissionView(View):
    def get(self, request, submission_id):
        try:
            api = SphereEngineAPI()
            result = api.get_submission(submission_id)
            print(f'i am from views{result}')
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class CompileCodeFormView(View):
   def get(self, request):
        api = SphereEngineAPI()
        compilers = api.get_compilers()
        compiler_list = compilers.get('items', [])

        return render(request, 'sphere_engine/compile_form.html', {'compilers': compiler_list})
    
    