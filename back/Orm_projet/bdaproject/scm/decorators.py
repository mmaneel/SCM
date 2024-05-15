import time
from functools import wraps
from django.http import JsonResponse
import json

def calculate_execution_time(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        start_time = time.time()
        response = view_func(request, *args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        if isinstance(response, JsonResponse):
            response_data = json.loads(response.content)
            response_data['execution_time'] = execution_time
            response = JsonResponse(response_data, status=response.status_code)
        return response
    return wrapped_view
