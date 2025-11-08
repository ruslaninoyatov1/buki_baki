from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    CategoryViewSet, VideoViewSet, ColoringViewSet, TaskViewSet,
    BannerViewSet, AdBlockViewSet, SubscriptionViewSet,
    user_profile, subscription_status, homepage_data
)

app_name = 'api'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'colorings', ColoringViewSet, basename='coloring')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'adblocks', AdBlockViewSet, basename='adblock')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    # REST API endpoints
    path('', include(router.urls)),
    
    # Custom API endpoints
    path('auth/profile/', user_profile, name='profile'),
    path('subscription/status/', subscription_status, name='subscription_status'),
    path('home/', homepage_data, name='home'),
    
    # Legacy endpoints
    path('auth/register/', views.api_register, name='register'),
    path('auth/login/', views.api_login, name='login'),
    path('auth/profile/legacy/', views.api_profile, name='profile_legacy'),
    path('categories/legacy/', views.api_categories, name='categories_legacy'),
    path('videos/legacy/', views.api_videos, name='videos_legacy'),
    path('videos/<int:video_id>/legacy/', views.api_video_detail, name='video_detail_legacy'),
    path('colorings/legacy/', views.api_colorings, name='colorings_legacy'),
    path('tasks/legacy/', views.api_tasks, name='tasks_legacy'),
    path('home/legacy/', views.api_home, name='home_legacy'),
    path('subscription/status/legacy/', views.api_subscription_status, name='subscription_status_legacy'),
    path('subscription/activate/', views.api_subscription_activate, name='subscription_activate'),
]

