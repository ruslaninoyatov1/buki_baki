from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.subscription.models import Subscription

@csrf_exempt
def profile(request):
    # Get user's subscription if they have one
    subscription = None
    if request.user.is_authenticated:
        try:
            subscription = Subscription.objects.get(user=request.user)
        except Subscription.DoesNotExist:
            subscription = None
    
    # Prepare subscription data
    subscription_data = None
    if subscription:
        subscription_data = {
            'id': subscription.id,
            'plan': subscription.plan,
            'description': subscription.description,
            'payment_platform': subscription.payment_platform,
            'start_date': subscription.start_date.isoformat(),
            'end_date': subscription.end_date.isoformat(),
            'is_active': subscription.is_active,
            'is_valid': subscription.is_valid
        }
    
    data = {
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        } if request.user.is_authenticated else None,
        'subscription': subscription_data,
        'status': 'success'
    }
    return JsonResponse(data)