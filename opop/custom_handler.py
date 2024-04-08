from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def custom_exception_handler(request, exception):
    if isinstance(exception, ObjectDoesNotExist):
        return JsonResponse({'error': 'Object not found'}, status=404)
    else:
        return JsonResponse({'error': str(exception)}, status=500)