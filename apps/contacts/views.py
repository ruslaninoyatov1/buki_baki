from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
import json

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            form = ContactForm(data)
        except json.JSONDecodeError:
            form = ContactForm(request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({
                'message': 'Thank you for your message. We will contact you soon.',
                'status': 'success'
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            return JsonResponse({
                'error': 'Form validation failed',
                'errors': errors,
                'status': 'error'
            }, status=400)
    
    return JsonResponse({
        'message': 'Contact API endpoint',
        'status': 'success'
    })