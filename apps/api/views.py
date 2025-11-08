from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .serializers import (
    VideoSerializer, ColoringSerializer, TaskSerializer,
    CategorySerializer, BannerSerializer, AdBlockSerializer,
    SubscriptionSerializer, UserSerializer
)
from apps.video.models import Video, VideoSeries
from apps.coloring.models import Coloring
from apps.tasks.models import Task
from apps.categories.models import Category
from apps.banners.models import Banner
from apps.ads.models import AdBlock
from apps.subscription.models import Subscription

# Category ViewSet
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

# Video ViewSet
class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Video.objects.all()
        category_slug = self.request.query_params.get('category', None)
        series_id = self.request.query_params.get('series', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if series_id:
            queryset = queryset.filter(series_group_id=series_id)
            
        return queryset.order_by('-date')

# Coloring ViewSet
class ColoringViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ColoringSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Coloring.objects.all()
        category_slug = self.request.query_params.get('category', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset.order_by('-created_at')

# Task ViewSet
class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Task.objects.all()
        category_slug = self.request.query_params.get('category', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset.order_by('-created_at')

# Banner ViewSet
class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_active=True).order_by('order', '-created_at')
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticated]

# AdBlock ViewSet
class AdBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdBlock.objects.filter(is_active=True).order_by('order', '-created_at')
    serializer_class = AdBlockSerializer
    permission_classes = [IsAuthenticated]

# Subscription ViewSet
class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

# User Profile API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Check subscription status
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    subscription = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    
    if subscription and subscription.is_valid:
        serializer = SubscriptionSerializer(subscription)
        return Response({
            'has_subscription': True,
            'subscription': serializer.data
        })
    else:
        return Response({
            'has_subscription': False,
            'subscription': None
        })

# Homepage data API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homepage_data(request):
    # Get active banners
    banners = Banner.objects.filter(is_active=True).order_by('order', '-created_at')[:5]
    banner_serializer = BannerSerializer(banners, many=True)
    
    # Get active ad blocks
    ad_blocks = AdBlock.objects.filter(is_active=True).order_by('order', '-created_at')[:3]
    ad_block_serializer = AdBlockSerializer(ad_blocks, many=True)
    
    # Get some videos, colorings, and tasks
    videos = Video.objects.all()[:6]
    video_serializer = VideoSerializer(videos, many=True)
    
    colorings = Coloring.objects.all()[:6]
    coloring_serializer = ColoringSerializer(colorings, many=True)
    
    tasks = Task.objects.all()[:6]
    task_serializer = TaskSerializer(tasks, many=True)
    
    return Response({
        'banners': banner_serializer.data,
        'ad_blocks': ad_block_serializer.data,
        'videos': video_serializer.data,
        'colorings': coloring_serializer.data,
        'tasks': task_serializer.data
    })


def get_user_subscription_status(user):
    """Check if user has active subscription or if category is free"""
    if not user or not user.is_authenticated:
        return False, None
    
    subscription = Subscription.objects.filter(
        user=user,
        is_active=True
    ).first()
    
    if subscription and subscription.is_valid:
        return True, subscription
    return False, None


def check_access(user, category):
    """Check if user has access to category"""
    if category.is_free:
        return True
    has_subscription, _ = get_user_subscription_status(user)
    return has_subscription


# Authentication API
@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """Register new user"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email', '')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return JsonResponse({
            'success': True,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'User registered successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Login user"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            has_subscription, subscription = get_user_subscription_status(user)
            
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'has_subscription': has_subscription
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["GET"])
def api_profile(request):
    """Get user profile"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    subscription_status, subscription = get_user_subscription_status(user)
    
    return JsonResponse({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined.isoformat(),
        },
        'subscription': {
            'has_subscription': subscription_status,
            'details': {
                'plan': subscription.plan if subscription else None,
                'start_date': subscription.start_date.isoformat() if subscription else None,
                'end_date': subscription.end_date.isoformat() if subscription else None,
                'is_valid': subscription.is_valid if subscription else False,
                'is_active': subscription.is_active if subscription else False,
            } if subscription else None
        }
    })


# Categories API
@require_http_methods(["GET"])
def api_categories(request):
    """Get all categories"""
    categories = Category.objects.all().order_by('title')
    
    has_subscription, _ = get_user_subscription_status(request.user if request.user.is_authenticated else None)
    
    categories_data = []
    for category in categories:
        has_access = category.is_free or has_subscription
        categories_data.append({
            'id': category.id,
            'title': category.title,
            'slug': category.slug,
            'is_free': category.is_free,
            'has_access': has_access
        })
    
    return JsonResponse({'categories': categories_data})


# Videos API
@require_http_methods(["GET"])
def api_videos(request):
    """Get videos by category or all videos"""
    category_slug = request.GET.get('category')
    series_id = request.GET.get('series')
    
    videos = Video.objects.all().order_by('-date')
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            if not check_access(request.user if request.user.is_authenticated else None, category):
                return JsonResponse({'error': 'Access denied. Subscription required.'}, status=403)
            videos = videos.filter(category=category)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
    
    if series_id:
        videos = videos.filter(series_group_id=series_id).order_by('order')
    
    videos_data = []
    for video in videos:
        try:
            preview_url = request.build_absolute_uri(video.preview.url) if video.preview else None
        except (ValueError, AttributeError):
            preview_url = None
        
        try:
            file_url = request.build_absolute_uri(video.file.url) if video.file else None
        except (ValueError, AttributeError):
            file_url = None
        
        videos_data.append({
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'preview': preview_url,
            'file': file_url,
            'category': {
                'id': video.category.id,
                'title': video.category.title,
                'slug': video.category.slug
            },
            'is_series': video.is_series,
            'series_group': {
                'id': video.series_group.id,
                'name': video.series_group.name
            } if video.series_group else None,
            'order': video.order,
            'date': video.date.isoformat()
        })
    
    return JsonResponse({'videos': videos_data})


@require_http_methods(["GET"])
def api_video_detail(request, video_id):
    """Get single video details"""
    try:
        video = Video.objects.get(id=video_id)
        
        if not check_access(request.user if request.user.is_authenticated else None, video.category):
            return JsonResponse({'error': 'Access denied. Subscription required.'}, status=403)
        
        # Get related videos if part of series
        related_videos = []
        if video.is_series and video.series_group:
            related_videos = Video.objects.filter(
                series_group=video.series_group
            ).exclude(id=video.id).order_by('order')
        
        try:
            preview_url = request.build_absolute_uri(video.preview.url) if video.preview else None
        except (ValueError, AttributeError):
            preview_url = None
        
        try:
            file_url = request.build_absolute_uri(video.file.url) if video.file else None
        except (ValueError, AttributeError):
            file_url = None
        
        data = {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'preview': preview_url,
            'file': file_url,
            'category': {
                'id': video.category.id,
                'title': video.category.title,
                'slug': video.category.slug
            },
            'is_series': video.is_series,
            'series_group': {
                'id': video.series_group.id,
                'name': video.series_group.name
            } if video.series_group else None,
            'related_videos': [
                {
                    'id': v.id,
                    'title': v.title,
                    'preview': (
                        request.build_absolute_uri(v.preview.url) 
                        if v.preview and hasattr(v.preview, 'url') 
                        else None
                    ),
                    'order': v.order
                } for v in related_videos
            ],
            'date': video.date.isoformat()
        }
        
        return JsonResponse(data)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)


# Colorings API
@require_http_methods(["GET"])
def api_colorings(request):
    """Get colorings by category or all colorings"""
    category_slug = request.GET.get('category')
    
    colorings = Coloring.objects.all().order_by('-created_at')
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            if not check_access(request.user if request.user.is_authenticated else None, category):
                return JsonResponse({'error': 'Access denied. Subscription required.'}, status=403)
            colorings = colorings.filter(category=category)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
    
    colorings_data = []
    for coloring in colorings:
        try:
            preview_url = request.build_absolute_uri(coloring.preview.url) if coloring.preview else None
        except (ValueError, AttributeError):
            preview_url = None
        
        try:
            file_url = request.build_absolute_uri(coloring.file.url) if coloring.file else None
        except (ValueError, AttributeError):
            file_url = None
        
        colorings_data.append({
            'id': coloring.id,
            'title': coloring.title,
            'preview': preview_url,
            'file': file_url,
            'category': {
                'id': coloring.category.id,
                'title': coloring.category.title,
                'slug': coloring.category.slug
            },
            'created_at': coloring.created_at.isoformat()
        })
    
    return JsonResponse({'colorings': colorings_data})


# Tasks API
@require_http_methods(["GET"])
def api_tasks(request):
    """Get tasks by category or all tasks"""
    category_slug = request.GET.get('category')
    
    tasks = Task.objects.all().order_by('-created_at')
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            if not check_access(request.user if request.user.is_authenticated else None, category):
                return JsonResponse({'error': 'Access denied. Subscription required.'}, status=403)
            tasks = tasks.filter(category=category)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
    
    tasks_data = []
    for task in tasks:
        try:
            preview_url = request.build_absolute_uri(task.preview.url) if task.preview else None
        except (ValueError, AttributeError):
            preview_url = None
        
        try:
            file_url = request.build_absolute_uri(task.file.url) if task.file else None
        except (ValueError, AttributeError):
            file_url = None
        
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'preview': preview_url,
            'file': file_url,
            'difficulty': task.difficulty,
            'age_group': task.age_group,
            'category': {
                'id': task.category.id,
                'title': task.category.title,
                'slug': task.category.slug
            },
            'created_at': task.created_at.isoformat()
        })
    
    return JsonResponse({'tasks': tasks_data})


# Homepage API
@require_http_methods(["GET"])
def api_home(request):
    """Get homepage data (banners and ad blocks)"""
    banners = Banner.objects.filter(is_active=True).order_by('order', '-created_at')
    ad_blocks = AdBlock.objects.filter(is_active=True).order_by('order', '-created_at')
    
    banners_data = []
    for banner in banners:
        try:
            image_url = request.build_absolute_uri(banner.image.url) if banner.image else None
        except (ValueError, AttributeError):
            image_url = None
        
        banners_data.append({
            'id': banner.id,
            'title': banner.title,
            'image': image_url,
            'link': banner.get_link()
        })
    
    ad_blocks_data = []
    for ad_block in ad_blocks:
        try:
            bg_image_url = request.build_absolute_uri(ad_block.background_image.url) if ad_block.background_image else None
        except (ValueError, AttributeError):
            bg_image_url = None
        
        ad_blocks_data.append({
            'id': ad_block.id,
            'title': ad_block.title,
            'background_image': bg_image_url,
            'content_type': ad_block.content_type,
            'link': ad_block.get_link()
        })
    
    return JsonResponse({
        'banners': banners_data,
        'ad_blocks': ad_blocks_data
    })


# Subscription API
@require_http_methods(["GET"])
def api_subscription_status(request):
    """Check subscription status"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    has_subscription, subscription = get_user_subscription_status(request.user)
    
    data = {
        'has_subscription': has_subscription,
        'subscription': None
    }
    
    if subscription:
        data['subscription'] = {
            'plan': subscription.plan,
            'payment_platform': subscription.payment_platform,
            'start_date': subscription.start_date.isoformat(),
            'end_date': subscription.end_date.isoformat(),
            'is_valid': subscription.is_valid
        }
    
    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Login user"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'message': 'Login successful'
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_subscription_activate(request):
    """
    Activate subscription for user
    This endpoint will be called by:
    - Google Play purchase verification
    - Apple App Store receipt validation
    - Admin manual activation
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        # Handle empty request body
        if not request.body:
            data = {}
        else:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                data = {}
        
        plan = data.get('plan', 'basic')
        payment_platform = data.get('payment_platform', 'web')
        months = data.get('months', 1)
        
        # Validate plan
        if plan not in ['basic', 'popular']:
            return JsonResponse({'error': 'Invalid plan'}, status=400)
        
        # Validate payment platform
        if payment_platform not in ['google_play', 'app_store', 'web']:
            return JsonResponse({'error': 'Invalid payment platform'}, status=400)
        
        # Get or create subscription
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            is_active=True,
            defaults={
                'plan': plan,
                'payment_platform': payment_platform,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=months * 30)
            }
        )
        
        if not created:
            # Renew existing subscription
            subscription.renew(months=months)
            subscription.plan = plan
            subscription.payment_platform = payment_platform
            subscription.save()
        
        # Store payment details if provided
        if data.get('google_play_order_id'):
            subscription.google_play_order_id = data.get('google_play_order_id')
        if data.get('app_store_transaction_id'):
            subscription.app_store_transaction_id = data.get('app_store_transaction_id')
        if data.get('purchase_token'):
            subscription.purchase_token = data.get('purchase_token')
        if data.get('receipt_data'):
            subscription.receipt_data = data.get('receipt_data')
        subscription.save()
        
        return JsonResponse({
            'success': True,
            'subscription': {
                'plan': subscription.plan,
                'payment_platform': subscription.payment_platform,
                'start_date': subscription.start_date.isoformat(),
                'end_date': subscription.end_date.isoformat(),
                'is_valid': subscription.is_valid
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
