import requests
from django.conf import settings
from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException
from sphere_engine import ProblemsClientV4

# logger = logging.getLogger(__name__)

class SphereEngineAPI:
    def __init__(self):
        self.compiler_access_token = settings.SPHERE_ENGINE_COMPILER_ACCESS_TOKEN
        self.problems_access_token = settings.SPHERE_ENGINE_PROBLEMS_ACCESS_TOKEN
        self.compiler_endpoint = f'https://{settings.SPHERE_ENGINE_COMPILER_ENDPOINT}/api/v4'
        self.compiler_endpoint_1 = f'https://{settings.SPHERE_ENGINE_COMPILER_ENDPOINT}/api/v4/submissions?'
        self.compiler_endpoint_2 = settings.SPHERE_ENGINE_COMPILER_ENDPOINT
        self.problems_endpoint_get = settings.SPHERE_ENGINE_PROBLEMS_ENDPOINT
        self.client = CompilersClientV4(self.compiler_access_token, self.compiler_endpoint_1)
        self.client_1 = CompilersClientV4(self.compiler_access_token, self.compiler_endpoint_2)
        self.client_problems = ProblemsClientV4(self.problems_access_token,self.problems_endpoint_get)

    # This is a test method 
    def test_authentication(self):
        url = f'{self.compiler_endpoint}/test?access_token={self.compiler_access_token}'
        response = requests.get(url)
        
        try:
            response_data = response.json()
        except ValueError:
            response_data = {
                'message': 'Invalid response format',
                'data': [],
                'error_code': response.status_code,
                'response_text': response.text
            }
        
        return response_data

    def get_headers(self, token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def get_compilers(self):
        url = f'{self.compiler_endpoint}/compilers?access_token={self.compiler_access_token}'
        response = requests.get(url)
        

        try:
            response_data = response.json()
        except ValueError:
            response_data = {
                'message': 'Invalid response format',
                'data': [],
                'error_code': response.status_code,
                'response_text': response.text
            }
        
        if response.status_code == 200:
            return response_data
        else:
            return {
                'message': 'Failed to fetch compilers',
                'data': response_data,
                'error_code': response.status_code
            }

    def compile_code(self, source_code, compiler_id, version_id):
        try:
            response = self.client.submissions.create(source_code, compiler_id)
            return response
        except SphereEngineException as e:
            if e.code == 401:
                return {'error': 'Invalid access token'}
            elif e.code == 402:
                return {'error': 'Unable to create submission'}
            elif e.code == 400:
                return {'error': f'Error code: {e.error_code}, details: {e}'}
            else:
                return {'error': f'An unknown error occurred {e}'}

    def get_submission_status(self, submission_id):
        url = f'{self.compiler_endpoint}/submissions/{submission_id}'
        headers = self.get_headers(self.compiler_access_token)
        response = requests.get(url, headers=headers)
        print(f'i am from get_submission_status {response}')
        return response.json()


    def get_submission(self, submission_id):
        try:
            print(f'I am from service {submission_id}')
            response = self.client_1.submissions.get(submission_id)
            print(response)
            return response
        except SphereEngineException as e:
            if e.code == 401:
                return {'error': 'Invalid access token'}
            elif e.code == 403:
                return {'error': 'Access to the submission is forbidden'}
            elif e.code == 404:
                return {'error': 'Submission does not exist'}
            else:
                return {'error': f'Error code: {e.code}, details: {e}'}

    def get_problems(self):
        try:
            print(f'Fetching all problems')
            response = self.client_problems.problems.all()
            return response
        except SphereEngineException as e:
            if e.code == 401:
                return {'error': 'Invalid access token'}
            elif e.code == 403:
                return {'error': 'Access to the submission is forbidden'}
            elif e.code == 404:
                return {'error': 'problems does not exist'}
            else:
                return {'error': f'Error code: {e.code}, details: {e}'}
            

    # def get_problem(self, problem_code):
    #     url = f'{self.problems_endpoint}/problems/{problem_code}'
    #     headers = self.get_headers(self.problems_access_token)
    #     response = requests.get(url, headers=headers)
    #     return response.json()
