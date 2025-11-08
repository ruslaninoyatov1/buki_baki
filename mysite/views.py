from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
import json

def index(request):
    """
    Serve the main index page
    """
    return render(request, 'index.html')

def blog(request):
    """
    Serve the blog page
    """
    return render(request, 'blog.html')

def post(request):
    """
    Serve the post page
    """
    return render(request, 'post.html')

def error_404(request, exception):
    """
    Error handler for 404
    """
    return render(request, '404.html', status=404)

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
        # For GET requests, you might want to serve a signup page
        # For now, we'll return a simple JSON response
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