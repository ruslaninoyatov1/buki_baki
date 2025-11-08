from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
import json

@csrf_exempt
def index(request):
    """
    API endpoint for homepage data
    """
    # Return JSON response instead of rendering template
    data = {
        'message': 'Kids Education Portal API',
        'status': 'success'
    }
    return JsonResponse(data)

@csrf_exempt
def blog(request):
    """
    API endpoint for blog data
    """
    data = {
        'message': 'Blog API endpoint',
        'status': 'success'
    }
    return JsonResponse(data)

@csrf_exempt
def post(request):
    """
    API endpoint for post data
    """
    data = {
        'message': 'Post API endpoint',
        'status': 'success'
    }
    return JsonResponse(data)

def error_404(request, exception):
    """
    API error handler
    """
    data = {
        'error': 'Not found',
        'status': 404
    }
    return JsonResponse(data, status=404)

@csrf_exempt
def signup(request):
    """
    API endpoint for user signup
    """
    if request.method == 'POST':
        # This would be implemented as an API endpoint
        data = {
            'message': 'Signup API endpoint',
            'status': 'success'
        }
        return JsonResponse(data)
    else:
        data = {
            'message': 'Signup API endpoint - GET request',
            'status': 'success'
        }
        return JsonResponse(data)

def test_translation(request):
    """
    API endpoint for testing translations
    """
    # Test translation
    translated_text = _("Kids Education Portal")
    data = {
        'translated_text': translated_text,
        'status': 'success'
    }
    return JsonResponse(data)