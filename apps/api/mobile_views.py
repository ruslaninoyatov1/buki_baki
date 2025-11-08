from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from apps.video.models import Video, VideoSeries
from apps.coloring.models import Coloring
from apps.tasks.models import Task
from apps.categories.models import Category
from apps.banners.models import Banner
from apps.ads.models import AdBlock
from apps.subscription.models import Subscription

def check_access(user, category):
    """Check if user has access to category"""
    if category.is_free:
        return True
    if not user or not user.is_authenticated:
        return False
    subscription = Subscription.objects.filter(
        user=user,
        is_active=True
    ).first()
    return subscription and subscription.is_valid if subscription else False


@csrf_exempt
def mobile_home(request):
    """Mobile homepage API - returns JSON data"""
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    # Try to get cached data first
    cache_key = f'mobile_home_{request.user.id}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        # Use cached data
        banners = cached_data['banners']
        ad_blocks = cached_data['ad_blocks']
        has_subscription = cached_data['has_subscription']
    else:
        # Get active banners
        banners_queryset = Banner.objects.filter(is_active=True).order_by('order', '-created_at')
        banners = []
        for banner in banners_queryset:
            banners.append({
                'id': banner.id,
                'title': banner.title,
                'description': banner.description,
                'image': banner.image.url if banner.image else None,
                'link': banner.get_link(),
                'created_at': banner.created_at.isoformat()
            })
        
        ad_blocks_queryset = AdBlock.objects.filter(is_active=True).order_by('order', '-created_at')
        ad_blocks = []
        for ad_block in ad_blocks_queryset:
            ad_blocks.append({
                'id': ad_block.id,
                'title': ad_block.title,
                'description': ad_block.description,
                'background_image': ad_block.background_image.url if ad_block.background_image else None,
                'content_type': ad_block.content_type,
                'link': ad_block.get_link(),
                'created_at': ad_block.created_at.isoformat()
            })
        
        subscription = Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).first()
        has_subscription = subscription and subscription.is_valid if subscription else False
        
        # Cache the data for 10 minutes
        cache_data = {
            'banners': banners,
            'ad_blocks': ad_blocks,
            'has_subscription': has_subscription,
        }
        cache.set(cache_key, cache_data, 60 * 10)  # Cache for 10 minutes
    
    data = {
        'banners': banners,
        'ad_blocks': ad_blocks,
        'has_subscription': has_subscription,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_login(request):
    """Mobile login API"""
    if request.user.is_authenticated:
        return JsonResponse({'message': 'Already authenticated', 'status': 'success'})
    
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            username = request.POST.get('username')
            password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'status': 'success'
            })
        else:
            return JsonResponse({'error': 'Invalid username or password', 'status': 'error'}, status=401)
    
    return JsonResponse({'message': 'Login endpoint', 'status': 'success'})


@csrf_exempt
def mobile_register(request):
    """Mobile registration API"""
    if request.user.is_authenticated:
        return JsonResponse({'message': 'Already authenticated', 'status': 'success'})
    
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email', '')
            password1 = data.get('password1')
            password2 = data.get('password2')
        except json.JSONDecodeError:
            username = request.POST.get('username')
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
        
        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match', 'status': 'error'}, status=400)
        elif User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists', 'status': 'error'}, status=400)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            login(request, user)
            return JsonResponse({
                'message': 'Registration successful!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'status': 'success'
            })
    
    return JsonResponse({'message': 'Registration endpoint', 'status': 'success'})


@csrf_exempt
def mobile_logout(request):
    """Mobile logout API"""
    logout(request)
    return JsonResponse({'message': 'Logout successful', 'status': 'success'})


@csrf_exempt
def mobile_categories(request):
    """Mobile categories API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    categories_queryset = Category.objects.all().order_by('title')
    
    subscription = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    has_subscription = subscription and subscription.is_valid if subscription else False
    
    categories_data = []
    for category in categories_queryset:
        has_access = category.is_free or has_subscription
        categories_data.append({
            'id': category.id,
            'title': category.title,
            'description': category.description,
            'slug': category.slug,
            'is_free': category.is_free,
            'has_access': has_access
        })
    
    data = {
        'categories_data': categories_data,
        'has_subscription': has_subscription,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_category_detail(request, slug):
    """Mobile category detail API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    category = get_object_or_404(Category, slug=slug)
    
    has_access = check_access(request.user, category)
    
    if not has_access:
        return JsonResponse({'error': 'Subscription required to access this category', 'status': 'error'}, status=403)
    
    videos_queryset = Video.objects.filter(category=category).order_by('-date')
    colorings_queryset = Coloring.objects.filter(category=category).order_by('-created_at')
    tasks_queryset = Task.objects.filter(category=category).order_by('-created_at')
    
    videos = []
    for video in videos_queryset:
        videos.append({
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'preview': video.preview.url if video.preview else None,
            'is_series': video.is_series,
            'date': video.date.isoformat()
        })
    
    colorings = []
    for coloring in colorings_queryset:
        colorings.append({
            'id': coloring.id,
            'title': coloring.title,
            'description': coloring.description,
            'preview': coloring.preview.url if coloring.preview else None,
            'created_at': coloring.created_at.isoformat()
        })
    
    tasks = []
    for task in tasks_queryset:
        tasks.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'preview': task.preview.url if task.preview else None,
            'difficulty': task.difficulty,
            'age_group': task.age_group,
            'created_at': task.created_at.isoformat()
        })
    
    data = {
        'category': {
            'id': category.id,
            'title': category.title,
            'description': category.description,
            'slug': category.slug,
            'is_free': category.is_free
        },
        'videos': videos,
        'colorings': colorings,
        'tasks': tasks,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_videos(request):
    """Mobile videos list API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    category_slug = request.GET.get('category')
    series_id = request.GET.get('series')
    
    videos_queryset = Video.objects.all().order_by('-date')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if not check_access(request.user, category):
            return JsonResponse({'error': 'Subscription required', 'status': 'error'}, status=403)
        videos_queryset = videos_queryset.filter(category=category)
    
    if series_id:
        videos_queryset = videos_queryset.filter(series_group_id=series_id).order_by('order')
    
    videos = []
    for video in videos_queryset:
        videos.append({
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'preview': video.preview.url if video.preview else None,
            'file': video.file.url if video.file else None,
            'category': {
                'id': video.category.id,
                'title': video.category.title,
                'slug': video.category.slug
            } if video.category else None,
            'is_series': video.is_series,
            'series_group': {
                'id': video.series_group.id,
                'name': video.series_group.name
            } if video.series_group else None,
            'order': video.order,
            'date': video.date.isoformat()
        })
    
    data = {
        'videos': videos,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_video_detail(request, video_id):
    """Mobile video detail API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    video = get_object_or_404(Video, id=video_id)
    
    if not check_access(request.user, video.category):
        return JsonResponse({'error': 'Subscription required', 'status': 'error'}, status=403)
    
    # Get related videos if part of series
    related_videos = []
    if video.is_series and video.series_group:
        related_videos_queryset = Video.objects.filter(
            series_group=video.series_group
        ).exclude(id=video.id).order_by('order')
        
        for related_video in related_videos_queryset:
            related_videos.append({
                'id': related_video.id,
                'title': related_video.title,
                'preview': related_video.preview.url if related_video.preview else None,
                'order': related_video.order,
                'date': related_video.date.isoformat()
            })
    
    data = {
        'video': {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'preview': video.preview.url if video.preview else None,
            'file': video.file.url if video.file else None,
            'category': {
                'id': video.category.id,
                'title': video.category.title,
                'slug': video.category.slug
            } if video.category else None,
            'is_series': video.is_series,
            'series_group': {
                'id': video.series_group.id,
                'name': video.series_group.name
            } if video.series_group else None,
            'order': video.order,
            'date': video.date.isoformat()
        },
        'related_videos': related_videos,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_colorings(request):
    """Mobile colorings list API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    category_slug = request.GET.get('category')
    
    colorings_queryset = Coloring.objects.all().order_by('-created_at')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if not check_access(request.user, category):
            return JsonResponse({'error': 'Subscription required', 'status': 'error'}, status=403)
        colorings_queryset = colorings_queryset.filter(category=category)
    
    colorings = []
    for coloring in colorings_queryset:
        colorings.append({
            'id': coloring.id,
            'title': coloring.title,
            'description': coloring.description,
            'preview': coloring.preview.url if coloring.preview else None,
            'file': coloring.file.url if coloring.file else None,
            'category': {
                'id': coloring.category.id,
                'title': coloring.category.title,
                'slug': coloring.category.slug
            } if coloring.category else None,
            'created_at': coloring.created_at.isoformat()
        })
    
    data = {
        'colorings': colorings,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_tasks(request):
    """Mobile tasks list API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    category_slug = request.GET.get('category')
    
    tasks_queryset = Task.objects.all().order_by('-created_at')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if not check_access(request.user, category):
            return JsonResponse({'error': 'Subscription required', 'status': 'error'}, status=403)
        tasks_queryset = tasks_queryset.filter(category=category)
    
    tasks = []
    for task in tasks_queryset:
        tasks.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'preview': task.preview.url if task.preview else None,
            'file': task.file.url if task.file else None,
            'difficulty': task.difficulty,
            'age_group': task.age_group,
            'category': {
                'id': task.category.id,
                'title': task.category.title,
                'slug': task.category.slug
            } if task.category else None,
            'created_at': task.created_at.isoformat()
        })
    
    data = {
        'tasks': tasks,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_profile(request):
    """Mobile profile API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    subscription = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    
    has_subscription = subscription and subscription.is_valid if subscription else False
    
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
        },
        'subscription': subscription_data,
        'has_subscription': has_subscription,
        'status': 'success'
    }
    return JsonResponse(data)


@csrf_exempt
def mobile_subscription(request):
    """Mobile subscription API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required', 'status': 'error'}, status=401)
    
    subscription = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    
    has_subscription = subscription and subscription.is_valid if subscription else False
    
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
        'subscription': subscription_data,
        'has_subscription': has_subscription,
        'status': 'success'
    }
    return JsonResponse(data)